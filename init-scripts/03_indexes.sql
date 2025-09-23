-- ============================================================
-- ÍNDICES RECOMENDADOS
-- ============================================================

-- ======================
-- GYMS
-- ======================
CREATE INDEX IF NOT EXISTS idx_gyms_name ON gyms (name);
CREATE INDEX IF NOT EXISTS idx_gyms_status ON gyms (status);
CREATE INDEX IF NOT EXISTS idx_gyms_is_active ON gyms (is_active);

-- ======================
-- BRANCHES
-- ======================
CREATE INDEX IF NOT EXISTS idx_branches_gym_id ON branches (gym_id);
CREATE INDEX IF NOT EXISTS idx_branches_status ON branches (status);
CREATE INDEX IF NOT EXISTS idx_branches_is_active ON branches (is_active);

-- ======================
-- CLIENTS
-- ======================
-- Búsqueda por apellidos o teléfono
CREATE INDEX IF NOT EXISTS idx_clients_last_name ON clients (last_name);
CREATE INDEX IF NOT EXISTS idx_clients_phone ON clients (phone);
CREATE INDEX IF NOT EXISTS idx_clients_status ON clients (status);

-- ======================
-- CLIENT BIOMETRICS
-- ======================
CREATE INDEX IF NOT EXISTS idx_client_biometrics_client_id ON client_biometrics (client_id);
-- Para búsquedas vectoriales con pgvector
CREATE INDEX IF NOT EXISTS idx_client_biometrics_embedding_hnsw
ON client_biometrics
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
-- ======================
-- PLANS
-- ======================
CREATE INDEX IF NOT EXISTS idx_plans_status ON plans (status);
CREATE INDEX IF NOT EXISTS idx_plans_is_available ON plans (is_available);

-- ======================
-- SUBSCRIPTIONS
-- ======================
CREATE INDEX IF NOT EXISTS idx_subscriptions_client_id ON subscriptions (client_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_plan_id ON subscriptions (plan_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions (status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_end_date ON subscriptions (end_date);

-- ======================
-- PAYMENTS
-- ======================
CREATE INDEX IF NOT EXISTS idx_payments_subscription_id ON payments (subscription_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments (status);
CREATE INDEX IF NOT EXISTS idx_payments_payment_date ON payments (payment_date);

-- ======================
-- ATTENDANCES
-- ======================
CREATE INDEX IF NOT EXISTS idx_attendances_client_id ON attendances (client_id);
CREATE INDEX IF NOT EXISTS idx_attendances_branch_id ON attendances (branch_id);
CREATE INDEX IF NOT EXISTS idx_attendances_check_in ON attendances (check_in);

-- ======================
-- CONSUMABLE MOVEMENTS
-- ======================
CREATE INDEX IF NOT EXISTS idx_movements_consumable_id ON consumable_movements (consumable_id);
CREATE INDEX IF NOT EXISTS idx_movements_branch_id ON consumable_movements (branch_id);
CREATE INDEX IF NOT EXISTS idx_movements_date ON consumable_movements (movement_date);

-- ======================
-- ASSETS
-- ======================
CREATE INDEX IF NOT EXISTS idx_assets_branch_id ON assets (branch_id);
CREATE INDEX IF NOT EXISTS idx_assets_status ON assets (status);

-- ======================
-- ASSET MAINTENANCE
-- ======================
CREATE INDEX IF NOT EXISTS idx_asset_maintenance_asset_id ON asset_maintenance (asset_id);
CREATE INDEX IF NOT EXISTS idx_asset_maintenance_date ON asset_maintenance (maintenance_date);
