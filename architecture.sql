/* =============================================================================
PROJECT: SHADOW-VENT (Forensic Data Pipeline)
ARCHITECT: Adel Alyafi
OBJECTIVE: Detect and isolate synthetic "Shadow" accounts in real-time.
=============================================================================
*/

-- --------------------------------------------------------------------------
-- 1. SILVER TIER: STAR SCHEMA DDL
-- Ensuring referential integrity and optimized JOIN performance.
-- --------------------------------------------------------------------------

CREATE TABLE dim_customers (
    user_id UUID PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    account_type VARCHAR(20)
);

CREATE TABLE dim_devices (
    device_id UUID PRIMARY KEY,
    ip_address VARCHAR(45)
);

CREATE TABLE fact_activity (
    activity_id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES dim_customers(user_id),
    device_id UUID REFERENCES dim_devices(device_id),
    initial_deposit DECIMAL(15,2),
    session_duration_sec INT,
    is_synthetic BOOLEAN
);

-- --------------------------------------------------------------------------
-- 2. GOLD TIER: ANALYTICS VIEW
-- Calculating "At-Risk Capital" for executive-level reporting.
-- --------------------------------------------------------------------------

CREATE OR REPLACE VIEW gold_fraud_summary AS 
SELECT 
    c.account_type, 
    COUNT(f.activity_id) as total_users, 
    SUM(CASE WHEN f.is_synthetic THEN 1 ELSE 0 END) as flagged_shadows, 
    SUM(f.initial_deposit) FILTER (WHERE f.is_synthetic) as at_risk_capital 
FROM fact_activity f 
JOIN dim_customers c ON f.user_id = c.user_id 
GROUP BY c.account_type;

-- --------------------------------------------------------------------------
-- 3. ACTIVE MITIGATION: THE "VENT"
-- Automating the bouncer logic using a PostgreSQL Trigger and Function.
-- --------------------------------------------------------------------------

CREATE TABLE fraud_quarantine (
    quarantine_id SERIAL PRIMARY KEY,
    user_id UUID,
    reason_flagged VARCHAR(255),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'Pending Review'
);

-- The Detection Brain: Identifies the "Zero-Jitter Elite" Signature (12s session)
CREATE OR REPLACE FUNCTION automatic_vent() RETURNS TRIGGER AS $$ 
BEGIN 
    IF EXISTS (
        SELECT 1 FROM dim_customers 
        WHERE user_id = NEW.user_id AND account_type = 'Elite'
    ) AND NEW.session_duration_sec = 12 
    THEN 
        INSERT INTO fraud_quarantine (user_id, reason_flagged) 
        VALUES (NEW.user_id, 'Automated Zero-Jitter Detection'); 
    END IF; 
    RETURN NEW; 
END; 
$$ LANGUAGE plpgsql;

-- The Reflex: Trigger fires on every new insert
CREATE TRIGGER filter_bots_on_insert 
AFTER INSERT ON fact_activity 
FOR EACH ROW 
EXECUTE FUNCTION automatic_vent();

-- --------------------------------------------------------------------------
-- 4. RECONCILIATION AUDIT
-- Verification query to ensure the system is catching bots accurately.
-- --------------------------------------------------------------------------
-- SELECT COUNT(*) FROM fraud_quarantine;
