-- ============================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- ============================================================

-- Insertar un gimnasio de ejemplo
INSERT INTO gyms (name, slug, description, email, phone) VALUES 
('FitZone Central', 'fitzone-central', 'Gimnasio principal con equipos de última generación', 'info@fitzone.com', '+57-300-123-4567');

-- Insertar una sucursal de ejemplo
INSERT INTO branches (gym_id, name, slug, address, phone, opening_hours) VALUES 
(1, 'FitZone Centro', 'fitzone-centro', 'Carrera 50 #30-45, Medellín', '+57-300-123-4567', 
 '{"monday": "5:00-22:00", "tuesday": "5:00-22:00", "wednesday": "5:00-22:00", "thursday": "5:00-22:00", "friday": "5:00-22:00", "saturday": "6:00-20:00", "sunday": "8:00-18:00"}'::jsonb);

-- Insertar un plan de ejemplo
INSERT INTO plans (name, slug, description, price, duration_unit, duration_count) VALUES 
('Plan Mensual', 'plan-mensual', 'Acceso completo por un mes', 80000.00, 'month', 1),
('Plan Anual', 'plan-anual', 'Acceso completo por un año con descuento', 800000.00, 'year', 1);

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE '✅ Schema creado exitosamente con % tablas', (
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
    );
END $$;
