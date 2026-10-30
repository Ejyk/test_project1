# database.py
import sqlite3
import secrets
from datetime import datetime


JOB_ID_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
JOB_ID_LENGTH = 5

def generate_unique_job_id(conn):
    while True:
        job_id = "".join(secrets.choice(JOB_ID_ALPHABET) for _ in range(JOB_ID_LENGTH))
        cur = conn.execute("SELECT 1 FROM jobs WHERE job_id = ?", (job_id,))
        if not cur.fetchone():
            return job_id

def normalize_job_id(job_id: str) -> str:
    return (job_id or "").strip().upper()


def generate_referral_code(length: int = 6) -> str:
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "EPMS-" + "".join(secrets.choice(alphabet) for _ in range(length))


DB_NAME = "jobs.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Jobs table
    c.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            client_name TEXT,
            client_email TEXT,
            trade TEXT,
            location TEXT,
            description TEXT,
            status TEXT,
            assigned_artisan TEXT,
            last_updated TEXT
        )
    """)

    # Artisans table
    # artisan_id is internal (autoincrement)
    # artisan_code is public random ID used to accept jobs
    c.execute("""
        CREATE TABLE IF NOT EXISTS artisans (
            artisan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            artisan_code TEXT UNIQUE,
            business_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            trade TEXT NOT NULL,
            location TEXT NOT NULL,
            approved INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# ✅ Migration: add description column if missing (safe to re-run)
def migrate_add_description():
    conn = get_connection()
    c = conn.cursor()

    c.execute("PRAGMA table_info(jobs)")
    columns = [row[1] for row in c.fetchall()]

    if "description" not in columns:
        c.execute("ALTER TABLE jobs ADD COLUMN description TEXT")
        conn.commit()

    conn.close()


# ✅ Migration: add artisan_code + active if missing (safe to re-run)
def migrate_add_artisan_code():
    conn = get_connection()
    c = conn.cursor()

    c.execute("PRAGMA table_info(artisans)")
    cols = [row[1] for row in c.fetchall()]

    if "artisan_code" not in cols:
        c.execute("ALTER TABLE artisans ADD COLUMN artisan_code TEXT")
        conn.commit()

    if "active" not in cols:
        c.execute("ALTER TABLE artisans ADD COLUMN active INTEGER DEFAULT 1")
        conn.commit()

    # Unique index (safe if rerun)
    try:
        c.execute("CREATE UNIQUE INDEX idx_artisan_code_unique ON artisans(artisan_code)")
        conn.commit()
    except Exception:
        pass

    conn.close()
    
    
# ✅ Migration: add referral system tables/columns
def migrate_add_referrals():
    conn = get_connection()
    c = conn.cursor()

    c.execute("PRAGMA table_info(artisans)")
    cols = [row[1] for row in c.fetchall()]

    if "referral_code" not in cols:
        c.execute("ALTER TABLE artisans ADD COLUMN referral_code TEXT")

    if "referred_by" not in cols:
        c.execute("ALTER TABLE artisans ADD COLUMN referred_by TEXT")

    try:
        c.execute("CREATE UNIQUE INDEX idx_referral_code_unique ON artisans(referral_code)")
    except Exception:
        pass

    c.execute("""
        CREATE TABLE IF NOT EXISTS referral_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_code TEXT,
            artisan_id INTEGER,
            amount REAL,
            paid INTEGER DEFAULT 0,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def _generate_candidate_code(length: int = 8) -> str:
    # Avoid confusing chars: 0/O and 1/I
    alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "EPMS-" + "".join(secrets.choice(alphabet) for _ in range(length))


def generate_unique_artisan_code(length: int = 8) -> str:
    """Generate a unique random artisan_code not already used in DB."""
    while True:
        code = _generate_candidate_code(length)
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT 1 FROM artisans WHERE artisan_code = ?", (code,))
        exists = c.fetchone()
        conn.close()
        if not exists:
            return code

def register_artisan(business_name, email, phone, trade, location, gas_safe_number=None, referred_by=None):
    """
    Insert artisan and return generated artisan_code.
    Prevents duplicate registration by email OR phone.
    """
    conn = get_connection()
    c = conn.cursor()

    # Check for existing artisan by email OR phone
    c.execute("""
        SELECT 1 FROM artisans
        WHERE email = ? OR phone = ?
    """, (email.strip().lower(), (phone or "").strip()))
    if c.fetchone():
        conn.close()
        raise ValueError("An artisan with this email or phone already exists.")

    artisan_code = generate_unique_artisan_code()
    referral_code = generate_referral_code()

    # Insert new artisan
    c.execute("""
        INSERT INTO artisans (
            artisan_code, business_name, email, phone, trade, location,
            approved, active, created_at, referral_code, referred_by, gas_safe_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        artisan_code,
        business_name.strip(),
        email.strip().lower(),
        (phone or "").strip(),
        trade,
        location.strip().title(),
        0,  # approved
        1,  # active
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        referral_code,
        referred_by,
        gas_safe_number
    ))

    conn.commit()
    conn.close()
    return artisan_code

            
