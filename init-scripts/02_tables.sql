-- ============================================================
-- GYMS Y SU ORGANIZACIÓN
-- ============================================================
CREATE TABLE gyms (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,

    name TEXT NOT NULL,
    slug TEXT UNIQUE, -- Para URLs amigables
    description TEXT,
    logo_url TEXT,
    website TEXT,
    email TEXT,
    phone TEXT,

    -- Campos de estado y control
    status record_status DEFAULT 'active' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,

    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Índices implícitos
    CONSTRAINT gyms_name_check CHECK (length(trim(name)) > 0),
    CONSTRAINT gym_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE TABLE branches (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    gym_id BIGINT NOT NULL REFERENCES gyms(id) ON DELETE CASCADE,

    name TEXT NOT NULL,
    slug TEXT UNIQUE,

    -- Dirección
    address TEXT,
    
    -- Contacto
    phone TEXT,
    email TEXT,

    -- Horarios (JSON para flexibilidad)
    opening_hours JSONB,
    
    -- Estado
    status record_status DEFAULT 'active' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,

    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,
    
    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb,

    CONSTRAINT branches_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- ============================================================
-- CLIENTES
-- ============================================================
CREATE TABLE clients (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    
    -- Identificación
    dni_type document_type NOT NULL,
    dni_number TEXT UNIQUE NOT NULL,
    
    -- Información personal
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    second_last_name TEXT,

    -- Contacto
    phone TEXT NOT NULL,
    alternative_phone TEXT,

    -- Información demográfica
    birth_date DATE NOT NULL,
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F', 'O')),
    
    -- Dirección
    address TEXT,

    -- Estado
    status record_status DEFAULT 'active' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,

    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,
    
    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb
);

-- ============================================================
-- DATOS BIOMETRICOS
-- ============================================================
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE client_biometrics (
       -- Identificación
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    client_id BIGINT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    
    -- Tipo y estado
    type biometric_type NOT NULL,
    
    -- Datos biométricos
    data BYTEA NOT NULL,                    -- imagen o huella original
    compressed_data BYTEA,                  -- versión comprimida para almacenamiento
    thumbnail BYTEA,                        -- miniatura para preview (solo para face)
    
    -- Embeddings y ML
    embedding vector(512),                  -- vector de características
    model_name TEXT,  -- modelo usado para generar embedding

    -- Seguridad y auditoría
    hash_checksum TEXT,                     -- hash para verificar integridad
    encryption_method TEXT,                 -- método de encriptación usado

    -- Estado y control
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,       -- biométrico principal para este tipo

    -- Auditoría completa
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    -- Metadatos extensibles
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Restricciones
    CONSTRAINT unique_client_biometric_active UNIQUE (client_id, type) DEFERRABLE INITIALLY DEFERRED
);

-- ============================================================
-- PLANES DE SUSCRIPCIÓN
-- ============================================================
CREATE TABLE plans (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    
    name TEXT NOT NULL,
    slug TEXT UNIQUE,
    description TEXT,
    short_description TEXT,
    
    -- Precios
    price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
    currency CHAR(3) DEFAULT 'COP',
    
    -- Duración
    duration_unit duration_type NOT NULL,
    duration_count INT NOT NULL,
    
    -- Disponibilidad
    is_available BOOLEAN DEFAULT TRUE,
    available_from DATE,
    available_until DATE,
    
    -- Estado
    status record_status DEFAULT 'active' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,

    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,
    
    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb
);

-- ============================================================
-- SUSCRIPCIONES
-- ============================================================
CREATE TABLE subscriptions (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    client_id BIGINT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    plan_id BIGINT NOT NULL REFERENCES plans(id) ON DELETE RESTRICT, -- No permitir eliminar plan con suscripciones
    
    -- Fechas
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- Precios al momento de la suscripción
    original_price NUMERIC(10,2) NOT NULL,
    discount_amount NUMERIC(10,2) DEFAULT 0,
    final_price NUMERIC(10,2) NOT NULL,
    
    -- Estado y control
    status subscription_status NOT NULL DEFAULT 'pending_payment',
    auto_renew BOOLEAN DEFAULT FALSE,

    -- Fechas importantes
    cancellation_date DATE,
    cancellation_reason TEXT,
    
    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT subscriptions_dates_check CHECK (end_date > start_date),
    CONSTRAINT subscriptions_price_check CHECK (final_price >= 0)
);

-- ============================================================
-- PAGOS
-- ============================================================
CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    subscription_id BIGINT NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,

    -- Información del pago
    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    currency CHAR(3) DEFAULT 'COP',
    payment_method payment_method NOT NULL,
    
    -- Estado y fechas
    status payment_status NOT NULL DEFAULT 'pending',
    payment_date TIMESTAMPTZ DEFAULT now(),
    
    -- Auditoría
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    
    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb
);

-- ============================================================
-- ASISTENCIAS
-- ============================================================
CREATE TABLE attendances (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    client_id BIGINT NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    branch_id BIGINT NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    
    -- Timestamps
    check_in TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Resultados
    result attendance_result NOT NULL,
    confidence_score DECIMAL(3,2), -- Para biometría
    
    -- Información del dispositivo/kiosco
    device_id TEXT,
    ip_address INET,
    
    -- Metadatos del reconocimiento
    biometric_type biometric_type,
    recognition_metadata JSONB,

    -- Metadatos
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE consumables (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,

    name TEXT NOT NULL,
    description TEXT,
    unit_type unit_measure NOT NULL,

    -- Audit
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb
);

-- ============================================================
-- INVENTARIO DE CONSUMIBLES
-- ============================================================

CREATE TABLE consumable_inventory (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,

    consumable_id BIGINT NOT NULL REFERENCES consumables(id) ON DELETE CASCADE,
    branch_id BIGINT NOT NULL REFERENCES branches(id) ON DELETE CASCADE,

    available_quantity NUMERIC(10,2) DEFAULT 0 NOT NULL,
    min_stock NUMERIC(10,2) DEFAULT 5.00,
    max_stock NUMERIC(10,2),

    -- Audit
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraint para validar que min_stock <= max_stock
    CONSTRAINT check_min_max_stock CHECK (min_stock <= max_stock OR max_stock IS NULL),

    -- Constraint para unique combination
    CONSTRAINT unique_consumable_branch UNIQUE (consumable_id, branch_id)
);

-- ============================================================
-- MOVIMIENTOS DE INVENTARIO
-- ============================================================

CREATE TABLE consumable_movements (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,

    consumable_id BIGINT NOT NULL REFERENCES consumables(id) ON DELETE CASCADE,
    branch_id BIGINT NOT NULL REFERENCES branches(id) ON DELETE CASCADE,

    movement_type inventory_movement_type NOT NULL,
    quantity NUMERIC(10,2) NOT NULL,
    movement_date TIMESTAMPTZ DEFAULT now() NOT NULL,
    responsible BIGINT,
    notes TEXT,

    -- Audit
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraint para validar que salidas sean negativas
    CONSTRAINT check_movement_quantity CHECK (
        (movement_type = 'entry' AND quantity > 0) OR
        (movement_type = 'exit' AND quantity < 0) OR
        (movement_type = 'adjustment') -- adjustments pueden ser positivos o negativos
    )
);

-- ============================================================
-- ACTIVOS
-- ============================================================

CREATE TABLE assets (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,

    name TEXT NOT NULL,
    description TEXT,
    purchase_date DATE,
    purchase_value NUMERIC(12,2),
    status asset_status DEFAULT 'operational',
    branch_id BIGINT NOT NULL REFERENCES branches(id) ON DELETE CASCADE,

    -- Audit
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    metadata JSONB DEFAULT '{}'::jsonb
);

-- ============================================================
-- MANTENIMIENTO DE ACTIVOS
-- ============================================================

CREATE TABLE asset_maintenance (
    id BIGSERIAL PRIMARY KEY,
    public_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,

    asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    maintenance_date DATE,
    maintenance_type maintenance_type,
    description TEXT,
    cost NUMERIC(12,2),

    status record_status DEFAULT 'active' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,

    -- Audit
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ,
    created_by BIGINT,
    updated_by BIGINT,

    metadata JSONB DEFAULT '{}'::jsonb
);