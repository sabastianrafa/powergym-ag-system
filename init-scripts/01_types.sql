CREATE TYPE duration_type AS ENUM (
    'day',      -- duración en días
    'week',     -- duración en semanas
    'month',    -- duración en meses
    'year'      -- duración en años
);

CREATE TYPE attendance_result AS ENUM (
    'recognized',       -- cliente reconocido y con suscripción activa
    'not_recognized',   -- cliente no reconocido
    'expired',          -- cliente reconocido pero su suscripción expiró
    'no_data'           -- no hay datos de embedding para el cliente
);

CREATE TYPE document_type AS ENUM (
    'CC', -- Cédula de Ciudadanía
    'TI', -- Tarjeta de Identidad
    'CE', -- Cédula de Extranjería
    'PP'  -- Pasaporte
);

CREATE TYPE record_status AS ENUM  (
    'active',    -- el registro está activo y en uso
    'inactive',  -- el registro está inactivo pero se conserva
    'archived',  -- el registro está archivado para referencia futura
    'deleted'    -- el registro ha sido eliminado lógicamente
);

CREATE TYPE biometric_type AS ENUM (
    'face',         -- reconocimiento facial
    'fingerprint'   -- reconocimiento por huella dactilar
);

CREATE TYPE subscription_status AS ENUM (
    'active',           -- el plan está vigente y pagado
    'expired',          -- terminó la fecha y no se renovó
    'pending_payment',  -- está en espera de pago
    'canceled'          -- el cliente canceló la suscripción
);

CREATE TYPE payment_method AS ENUM (
    'cash',  -- pago en efectivo
    'qr'     -- pago mediante código QR
);

CREATE TYPE payment_status AS ENUM (
    'pending',    -- el pago está en proceso
    'completed',  -- el pago se realizó con éxito
    'failed'      -- el pago falló
);

CREATE TYPE unit_measure AS ENUM (
    'bottle',   -- botellas
    'can',      -- latas
    'bag',      -- bolsas
    'jar',      -- tarros/frascos
    'box'      -- cajas
);

CREATE TYPE inventory_movement_type AS ENUM (
    'entry',    -- entrada
    'exit',     -- salida
    'adjustment'-- ajuste
);

CREATE TYPE asset_status AS ENUM (
    'operational',   -- operativo
    'maintenance',   -- en mantenimiento
    'retired'        -- retirado de servicio
);

CREATE TYPE maintenance_type AS ENUM (
    'preventive',    -- mantenimiento preventivo
    'corrective'     -- mantenimiento correctivo
);