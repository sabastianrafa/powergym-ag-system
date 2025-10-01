export enum BiometricType {
  FINGERPRINT = 'FINGERPRINT',
  FACE = 'FACE',
  IRIS = 'IRIS',
  VOICE = 'VOICE',
  OTHER = 'OTHER'
}

export interface Biometric {
  id: string;
  customer_id: string;
  biometric_type: BiometricType;
  template_data?: string;
  embedding_vector?: number[];
  raw_image_url?: string;
  quality_score?: number;
  is_primary: boolean;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface BiometricFormData {
  customer_id: string;
  biometric_type: BiometricType;
  template_data?: string;
  embedding_vector?: number[];
  raw_image_url?: string;
  quality_score?: number;
  is_primary?: boolean;
  metadata?: Record<string, any>;
}

export interface BiometricUploadData {
  customer_id: string;
  biometric_type: BiometricType;
  file: File;
  quality_score?: number;
  is_primary?: boolean;
  metadata?: Record<string, any>;
}
