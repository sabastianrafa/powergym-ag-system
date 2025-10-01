import React, { useState } from 'react';
import { X, Upload } from 'lucide-react';
import { Select } from '../ui/Select';
import { FileUpload } from '../ui/FileUpload';
import { biometricsAPI } from '../../services/api';
import { useToast } from '../../hooks/useToast';

interface BiometricRegistrationModalProps {
  isOpen: boolean;
  onClose: () => void;
  customerId: string;
  onSuccess: () => void;
}

const BIOMETRIC_TYPE_OPTIONS = [
  { value: 'fingerprint', label: 'Huella Dactilar' },
  { value: 'face', label: 'Reconocimiento Facial' },
];

export const BiometricRegistrationModal: React.FC<BiometricRegistrationModalProps> = ({
  isOpen,
  onClose,
  customerId,
  onSuccess,
}) => {
  const { success, error } = useToast();
  const [biometricType, setBiometricType] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [isPrimary, setIsPrimary] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{ type?: string; file?: string }>({});

  const handleSubmit = async () => {
    const newErrors: { type?: string; file?: string } = {};

    if (!biometricType) {
      newErrors.type = 'Tipo de biométrico es requerido';
    }

    if (!file) {
      newErrors.file = 'Archivo es requerido';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsSubmitting(true);
    try {
      await biometricsAPI.upload({
        customer_id: customerId,
        biometric_type: biometricType as 'fingerprint' | 'face',
        file: file!,
        is_primary: isPrimary,
      });

      success('Dato biométrico registrado exitosamente');
      onSuccess();
      handleClose();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Error al registrar biométrico');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setBiometricType('');
    setFile(null);
    setIsPrimary(false);
    setErrors({});
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Registrar Dato Biométrico</h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600"
            disabled={isSubmitting}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          <Select
            label="Tipo de Biométrico"
            options={BIOMETRIC_TYPE_OPTIONS}
            value={biometricType}
            onChange={(e) => {
              setBiometricType(e.target.value);
              if (errors.type) setErrors((prev) => ({ ...prev, type: undefined }));
            }}
            error={errors.type}
            required
          />

          <FileUpload
            label="Archivo Biométrico"
            accept={biometricType === 'face' ? 'image/*' : '*'}
            value={file}
            onChange={(newFile) => {
              setFile(newFile);
              if (errors.file) setErrors((prev) => ({ ...prev, file: undefined }));
            }}
            error={errors.file}
            preview={biometricType === 'face'}
            helperText={
              biometricType === 'face'
                ? 'Sube una imagen del rostro (JPG, PNG)'
                : 'Sube el archivo de huella dactilar'
            }
          />

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isPrimary"
              checked={isPrimary}
              onChange={(e) => setIsPrimary(e.target.checked)}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="isPrimary" className="text-sm text-gray-700">
              Marcar como dato biométrico principal
            </label>
          </div>

          {file && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
              <div className="flex items-start gap-2">
                <Upload className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-blue-900">Archivo Seleccionado</p>
                  <p className="text-xs text-blue-700 mt-1">{file.name}</p>
                  <p className="text-xs text-blue-600 mt-1">
                    Tamaño: {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="flex gap-3 px-6 py-4 bg-gray-50 rounded-b-lg border-t border-gray-200">
          <button
            onClick={handleClose}
            disabled={isSubmitting}
            className="flex-1 px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Cancelar
          </button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="flex-1 px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {isSubmitting ? 'Registrando...' : 'Registrar'}
          </button>
        </div>
      </div>
    </div>
  );
};
