export enum DocumentType {
  DNI = 'DNI',
  CE = 'CE',
  PASSPORT = 'PASSPORT',
  OTHER = 'OTHER'
}

export enum GenderType {
  MALE = 'MALE',
  FEMALE = 'FEMALE',
  OTHER = 'OTHER'
}

export enum RecordStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED'
}

export interface Customer {
  id: string;
  dni_type: DocumentType;
  dni_number: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  second_last_name?: string;
  birth_date: string;
  gender: GenderType;
  email?: string;
  phone?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  photo_url?: string;
  notes?: string;
  status: RecordStatus;
  created_at: string;
  updated_at: string;
}

export interface CustomerFormData {
  dni_type: DocumentType;
  dni_number: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  second_last_name?: string;
  birth_date: string;
  gender: GenderType;
  email?: string;
  phone?: string;
  address?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  photo_url?: string;
  notes?: string;
  status?: RecordStatus;
}
