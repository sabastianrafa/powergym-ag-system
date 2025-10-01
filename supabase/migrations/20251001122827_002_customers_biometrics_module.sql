/*
  # Módulo de Administración de Clientes y Biometría

  1. Tipos Enumerados
    - `document_type`: Tipos de documentos de identidad (CC, TI, CE, PP)
    - `gender_type`: Género (M, F, O)
    - `record_status`: Estado de registros (active, inactive, archived, deleted)
    - `biometric_type`: Tipos de biometría (face, fingerprint)

  2. Extensiones
    - `vector`: Para almacenar embeddings de ML

  3. Tablas Nuevas
    - `customers`: Datos personales y de contacto de clientes
      - `id` (uuid): Identificador único
      - `dni_type` (document_type): Tipo de documento
      - `dni_number` (text): Número de documento único
      - `first_name` (text): Primer nombre
      - `middle_name` (text): Segundo nombre (opcional)
      - `last_name` (text): Primer apellido
      - `second_last_name` (text): Segundo apellido (opcional)
      - `phone` (text): Teléfono principal
      - `alternative_phone` (text): Teléfono alternativo (opcional)
      - `birth_date` (date): Fecha de nacimiento
      - `gender` (gender_type): Género
      - `address` (text): Dirección (opcional)
      - `status` (record_status): Estado del registro
      - `is_active` (boolean): Indica si está activo
      - `created_at` (timestamptz): Fecha de creación
      - `updated_at` (timestamptz): Fecha de actualización
      - `meta_info` (jsonb): Metadatos extensibles

    - `client_biometrics`: Datos biométricos de clientes
      - `id` (uuid): Identificador único
      - `client_id` (uuid): Referencia al cliente
      - `type` (biometric_type): Tipo de dato biométrico
      - `data` (bytea): Imagen o huella original
      - `compressed_data` (bytea): Versión comprimida
      - `thumbnail` (bytea): Miniatura para preview
      - `embedding` (vector): Vector de características ML
      - `hash_checksum` (text): Hash para verificar integridad
      - `encryption_method` (text): Método de encriptación usado
      - `is_active` (boolean): Indica si está activo
      - `created_at` (timestamptz): Fecha de creación
      - `updated_at` (timestamptz): Fecha de actualización
      - `meta_info` (jsonb): Metadatos extensibles

  4. Seguridad
    - RLS habilitado en ambas tablas
    - Políticas restrictivas para usuarios autenticados
    - Control de acceso basado en autenticación

  5. Índices
    - Índices para búsqueda eficiente por DNI, estado, cliente
    - Índice para embeddings vectoriales

  6. Triggers
    - Actualización automática de `updated_at`
*/

-- ============================================================
-- TIPOS ENUMERADOS
-- ============================================================

DO $$ BEGIN
    CREATE TYPE document_type AS ENUM (
        'CC', -- Cédula de Ciudadanía
        'TI', -- Tarjeta de Identidad
        'CE', -- Cédula de Extranjería
        'PP'  -- Pasaporte
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE gender_type AS ENUM (
        'M', -- Masculino
        'F', -- Femenino
        'O'  -- Otro
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE record_status AS ENUM (
        'active',    -- el registro está activo y en uso
        'inactive',  -- el registro está inactivo pero se conserva
        'archived',  -- el registro está archivado para referencia futura
        'deleted'    -- el registro ha sido eliminado lógicamente
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE biometric_type AS ENUM (
        'face',         -- reconocimiento facial
        'fingerprint'   -- reconocimiento por huella dactilar
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ============================================================
-- EXTENSIONES
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- TABLA DE CLIENTES
-- ============================================================

-- Primero verificamos si la tabla tiene la estructura antigua o nueva
DO $$
BEGIN
  -- Si la tabla no existe, la creamos con la nueva estructura
  IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'customers') THEN
    CREATE TABLE customers (
      id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      dni_type document_type NOT NULL,
      dni_number TEXT UNIQUE NOT NULL,
      first_name TEXT NOT NULL,
      middle_name TEXT,
      last_name TEXT NOT NULL,
      second_last_name TEXT,
      phone TEXT NOT NULL,
      alternative_phone TEXT,
      birth_date DATE NOT NULL,
      gender gender_type NOT NULL,
      address TEXT,
      status record_status DEFAULT 'active' NOT NULL,
      is_active BOOLEAN DEFAULT TRUE NOT NULL,
      created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
      updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
      meta_info JSONB DEFAULT '{}'::jsonb
    );
  ELSE
    -- Si existe pero tiene la estructura antigua, necesitamos migrar
    IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'dni') THEN
      -- Renombrar columna dni a dni_number
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'dni_number') THEN
        ALTER TABLE customers RENAME COLUMN dni TO dni_number;
      END IF;

      -- Agregar columna dni_type
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'dni_type') THEN
        ALTER TABLE customers ADD COLUMN dni_type document_type DEFAULT 'CC' NOT NULL;
      END IF;

      -- Agregar columna middle_name
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'middle_name') THEN
        ALTER TABLE customers ADD COLUMN middle_name TEXT;
      END IF;

      -- Agregar columna second_last_name
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'second_last_name') THEN
        ALTER TABLE customers ADD COLUMN second_last_name TEXT;
      END IF;

      -- Agregar columna alternative_phone
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'alternative_phone') THEN
        ALTER TABLE customers ADD COLUMN alternative_phone TEXT;
      END IF;

      -- Renombrar date_of_birth a birth_date
      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'date_of_birth') THEN
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'birth_date') THEN
          ALTER TABLE customers RENAME COLUMN date_of_birth TO birth_date;
        END IF;
      END IF;

      -- Agregar columna gender
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'gender') THEN
        ALTER TABLE customers ADD COLUMN gender gender_type DEFAULT 'O' NOT NULL;
      END IF;

      -- Cambiar tipo de columna status si es necesario
      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'status' AND udt_name = 'customer_status') THEN
        ALTER TABLE customers ALTER COLUMN status DROP DEFAULT;
        ALTER TABLE customers ALTER COLUMN status TYPE record_status USING
          CASE
            WHEN status::text = 'active' THEN 'active'::record_status
            WHEN status::text = 'inactive' THEN 'inactive'::record_status
            ELSE 'active'::record_status
          END;
        ALTER TABLE customers ALTER COLUMN status SET DEFAULT 'active'::record_status;
        ALTER TABLE customers ALTER COLUMN status SET NOT NULL;
      END IF;

      -- Agregar columna is_active
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'is_active') THEN
        ALTER TABLE customers ADD COLUMN is_active BOOLEAN DEFAULT TRUE NOT NULL;
      END IF;

      -- Agregar columna meta_info
      IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'meta_info') THEN
        ALTER TABLE customers ADD COLUMN meta_info JSONB DEFAULT '{}'::jsonb;
      END IF;

      -- Eliminar columnas legacy que ya no se necesitan
      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'email') THEN
        ALTER TABLE customers DROP COLUMN IF EXISTS email;
      END IF;

      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'emergency_contact_name') THEN
        ALTER TABLE customers DROP COLUMN IF EXISTS emergency_contact_name;
      END IF;

      IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'customers' AND column_name = 'emergency_contact_phone') THEN
        ALTER TABLE customers DROP COLUMN IF EXISTS emergency_contact_phone;
      END IF;
    END IF;
  END IF;
END $$;

-- Índices para customers
DROP INDEX IF EXISTS idx_customers_dni;
CREATE INDEX IF NOT EXISTS idx_customers_dni_number ON customers(dni_number);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_customers_is_active ON customers(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_customers_created_at ON customers(created_at DESC);

-- ============================================================
-- TABLA DE DATOS BIOMÉTRICOS
-- ============================================================

CREATE TABLE IF NOT EXISTS client_biometrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    
    type biometric_type NOT NULL,
    
    data BYTEA NOT NULL,
    compressed_data BYTEA,
    thumbnail BYTEA,
    
    embedding vector(512),
    
    hash_checksum TEXT,
    encryption_method TEXT,
    
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    
    meta_info JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT unique_client_biometric_active UNIQUE (client_id, type) DEFERRABLE INITIALLY DEFERRED
);

-- Índices para client_biometrics
CREATE INDEX IF NOT EXISTS idx_client_biometrics_client_id ON client_biometrics(client_id);
CREATE INDEX IF NOT EXISTS idx_client_biometrics_type ON client_biometrics(type);
CREATE INDEX IF NOT EXISTS idx_client_biometrics_is_active ON client_biometrics(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_client_biometrics_embedding ON client_biometrics USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- ============================================================
-- TRIGGERS PARA UPDATED_AT
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_customers_updated_at ON customers;
CREATE TRIGGER update_customers_updated_at
    BEFORE UPDATE ON customers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_client_biometrics_updated_at ON client_biometrics;
CREATE TRIGGER update_client_biometrics_updated_at
    BEFORE UPDATE ON client_biometrics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- SEGURIDAD - ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE client_biometrics ENABLE ROW LEVEL SECURITY;

-- Políticas para customers
DROP POLICY IF EXISTS "Authenticated users can view customers" ON customers;
CREATE POLICY "Authenticated users can view customers"
    ON customers FOR SELECT
    TO authenticated
    USING (true);

DROP POLICY IF EXISTS "Authenticated users can insert customers" ON customers;
CREATE POLICY "Authenticated users can insert customers"
    ON customers FOR INSERT
    TO authenticated
    WITH CHECK (true);

DROP POLICY IF EXISTS "Authenticated users can update customers" ON customers;
CREATE POLICY "Authenticated users can update customers"
    ON customers FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Authenticated users can delete customers" ON customers;
CREATE POLICY "Authenticated users can delete customers"
    ON customers FOR DELETE
    TO authenticated
    USING (true);

-- Políticas para client_biometrics
DROP POLICY IF EXISTS "Authenticated users can view biometrics" ON client_biometrics;
CREATE POLICY "Authenticated users can view biometrics"
    ON client_biometrics FOR SELECT
    TO authenticated
    USING (true);

DROP POLICY IF EXISTS "Authenticated users can insert biometrics" ON client_biometrics;
CREATE POLICY "Authenticated users can insert biometrics"
    ON client_biometrics FOR INSERT
    TO authenticated
    WITH CHECK (true);

DROP POLICY IF EXISTS "Authenticated users can update biometrics" ON client_biometrics;
CREATE POLICY "Authenticated users can update biometrics"
    ON client_biometrics FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

DROP POLICY IF EXISTS "Authenticated users can delete biometrics" ON client_biometrics;
CREATE POLICY "Authenticated users can delete biometrics"
    ON client_biometrics FOR DELETE
    TO authenticated
    USING (true);