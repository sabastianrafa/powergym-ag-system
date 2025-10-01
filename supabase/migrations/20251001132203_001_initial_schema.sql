/*
  # Initial Schema for PowerGym Management System

  ## Overview
  This migration creates the complete database schema for a gym management system
  with authentication, customer management, plans, subscriptions, payments, and attendance tracking.

  ## 1. New Tables

  ### `user_roles`
  Stores the role assignment for authenticated users.
  - `user_id` (uuid, primary key, references auth.users)
  - `role` (enum: 'admin', 'employee')
  - `created_at` (timestamptz)

  ### `customers`
  Stores gym customer information.
  - `id` (uuid, primary key)
  - `dni` (text, unique) - National identification number
  - `first_name` (text)
  - `last_name` (text)
  - `email` (text, unique)
  - `phone` (text)
  - `date_of_birth` (date)
  - `address` (text)
  - `emergency_contact_name` (text)
  - `emergency_contact_phone` (text)
  - `status` (enum: 'active', 'inactive')
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ### `plans`
  Defines available subscription plans.
  - `id` (uuid, primary key)
  - `name` (text)
  - `description` (text)
  - `duration_days` (integer) - Plan duration in days
  - `price` (numeric)
  - `is_active` (boolean)
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ### `subscriptions`
  Tracks customer subscriptions to plans.
  - `id` (uuid, primary key)
  - `customer_id` (uuid, references customers)
  - `plan_id` (uuid, references plans)
  - `start_date` (date)
  - `end_date` (date)
  - `status` (enum: 'active', 'expired', 'cancelled')
  - `created_at` (timestamptz)
  - `updated_at` (timestamptz)

  ### `payments`
  Records payment transactions.
  - `id` (uuid, primary key)
  - `subscription_id` (uuid, references subscriptions)
  - `customer_id` (uuid, references customers)
  - `amount` (numeric)
  - `payment_date` (timestamptz)
  - `payment_method` (enum: 'cash', 'credit_card', 'debit_card', 'transfer')
  - `status` (enum: 'completed', 'pending', 'cancelled')
  - `notes` (text)
  - `created_at` (timestamptz)

  ### `attendances`
  Logs customer check-ins.
  - `id` (uuid, primary key)
  - `customer_id` (uuid, references customers)
  - `check_in_time` (timestamptz)
  - `created_at` (timestamptz)

  ## 2. Security
  - Enable RLS on all tables
  - Create policies for authenticated users based on roles
  - Admin users have full access to all tables
  - Employee users have limited access (read customers, manage attendances)
  - Customers data is protected and only accessible by authenticated staff
  - Service role can insert user roles for seeding purposes

  ## 3. Indexes
  - Add indexes on foreign keys for better query performance
  - Add indexes on frequently searched fields (dni, email)
*/

-- Create custom types (enums)
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
    CREATE TYPE user_role AS ENUM ('admin', 'employee');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'customer_status') THEN
    CREATE TYPE customer_status AS ENUM ('active', 'inactive');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'subscription_status') THEN
    CREATE TYPE subscription_status AS ENUM ('active', 'expired', 'cancelled');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_method') THEN
    CREATE TYPE payment_method AS ENUM ('cash', 'credit_card', 'debit_card', 'transfer');
  END IF;
END $$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_status') THEN
    CREATE TYPE payment_status AS ENUM ('completed', 'pending', 'cancelled');
  END IF;
END $$;

-- Create user_roles table
CREATE TABLE IF NOT EXISTS user_roles (
  user_id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  role user_role NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create customers table (legacy version - will be updated in migration 002)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'customers') THEN
    CREATE TABLE customers (
      id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
      dni text UNIQUE NOT NULL,
      first_name text NOT NULL,
      last_name text NOT NULL,
      email text UNIQUE NOT NULL,
      phone text NOT NULL,
      date_of_birth date NOT NULL,
      address text,
      emergency_contact_name text,
      emergency_contact_phone text,
      status customer_status DEFAULT 'active',
      created_at timestamptz DEFAULT now(),
      updated_at timestamptz DEFAULT now()
    );
  END IF;
END $$;

-- Create plans table
CREATE TABLE IF NOT EXISTS plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  description text,
  duration_days integer NOT NULL CHECK (duration_days > 0),
  price numeric(10, 2) NOT NULL CHECK (price >= 0),
  is_active boolean DEFAULT true,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id uuid NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  plan_id uuid NOT NULL REFERENCES plans(id) ON DELETE RESTRICT,
  start_date date NOT NULL,
  end_date date NOT NULL,
  status subscription_status DEFAULT 'active',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create payments table
CREATE TABLE IF NOT EXISTS payments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id uuid NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  customer_id uuid NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  amount numeric(10, 2) NOT NULL CHECK (amount >= 0),
  payment_date timestamptz DEFAULT now(),
  payment_method payment_method NOT NULL,
  status payment_status DEFAULT 'completed',
  notes text,
  created_at timestamptz DEFAULT now()
);

-- Create attendances table
CREATE TABLE IF NOT EXISTS attendances (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id uuid NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  check_in_time timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_customers_dni ON customers(dni);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_customer_id ON subscriptions(customer_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_payments_customer_id ON payments(customer_id);
CREATE INDEX IF NOT EXISTS idx_payments_subscription_id ON payments(subscription_id);
CREATE INDEX IF NOT EXISTS idx_attendances_customer_id ON attendances(customer_id);
CREATE INDEX IF NOT EXISTS idx_attendances_check_in_time ON attendances(check_in_time);

-- Enable Row Level Security
ALTER TABLE user_roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendances ENABLE ROW LEVEL SECURITY;

-- RLS Policies for user_roles
DROP POLICY IF EXISTS "Authenticated users can view their own role" ON user_roles;
CREATE POLICY "Authenticated users can view their own role"
  ON user_roles FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Service role can insert user roles" ON user_roles;
CREATE POLICY "Service role can insert user roles"
  ON user_roles FOR INSERT
  WITH CHECK (true);

-- RLS Policies for customers
DROP POLICY IF EXISTS "Authenticated staff can view all customers" ON customers;
CREATE POLICY "Authenticated staff can view all customers"
  ON customers FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Only admins can insert customers" ON customers;
CREATE POLICY "Only admins can insert customers"
  ON customers FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can update customers" ON customers;
CREATE POLICY "Only admins can update customers"
  ON customers FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can delete customers" ON customers;
CREATE POLICY "Only admins can delete customers"
  ON customers FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

-- RLS Policies for plans
DROP POLICY IF EXISTS "Authenticated staff can view plans" ON plans;
CREATE POLICY "Authenticated staff can view plans"
  ON plans FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Only admins can insert plans" ON plans;
CREATE POLICY "Only admins can insert plans"
  ON plans FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can update plans" ON plans;
CREATE POLICY "Only admins can update plans"
  ON plans FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can delete plans" ON plans;
CREATE POLICY "Only admins can delete plans"
  ON plans FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

-- RLS Policies for subscriptions
DROP POLICY IF EXISTS "Authenticated staff can view subscriptions" ON subscriptions;
CREATE POLICY "Authenticated staff can view subscriptions"
  ON subscriptions FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Only admins can insert subscriptions" ON subscriptions;
CREATE POLICY "Only admins can insert subscriptions"
  ON subscriptions FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can update subscriptions" ON subscriptions;
CREATE POLICY "Only admins can update subscriptions"
  ON subscriptions FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can delete subscriptions" ON subscriptions;
CREATE POLICY "Only admins can delete subscriptions"
  ON subscriptions FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

-- RLS Policies for payments
DROP POLICY IF EXISTS "Authenticated staff can view payments" ON payments;
CREATE POLICY "Authenticated staff can view payments"
  ON payments FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Authenticated staff can insert payments" ON payments;
CREATE POLICY "Authenticated staff can insert payments"
  ON payments FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Only admins can update payments" ON payments;
CREATE POLICY "Only admins can update payments"
  ON payments FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

DROP POLICY IF EXISTS "Only admins can delete payments" ON payments;
CREATE POLICY "Only admins can delete payments"
  ON payments FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );

-- RLS Policies for attendances
DROP POLICY IF EXISTS "Authenticated staff can view attendances" ON attendances;
CREATE POLICY "Authenticated staff can view attendances"
  ON attendances FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Authenticated staff can insert attendances" ON attendances;
CREATE POLICY "Authenticated staff can insert attendances"
  ON attendances FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role IN ('admin', 'employee')
    )
  );

DROP POLICY IF EXISTS "Only admins can delete attendances" ON attendances;
CREATE POLICY "Only admins can delete attendances"
  ON attendances FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM user_roles
      WHERE user_roles.user_id = auth.uid()
      AND user_roles.role = 'admin'
    )
  );
