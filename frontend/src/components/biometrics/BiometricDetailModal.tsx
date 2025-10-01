import React from 'react';
import { X, Fingerprint, Image as ImageIcon } from 'lucide-react';
import { Biometric } from '../../types/biometric';
import { StatusBadge } from '../ui/StatusBadge';

interface BiometricDetailModalProps {
  biometric: Biometric;
  onClose: () => void;
}

export const BiometricDetailModal: React.FC<BiometricDetailModalProps> = ({
  biometric,
  onClose,
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <Fingerprint className="text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">Detalles del Biométrico</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              {biometric.biometric_type === 'face' ? (
                <ImageIcon className="w-5 h-5 text-gray-600" />
              ) : (
                <Fingerprint className="w-5 h-5 text-gray-600" />
              )}
              <h3 className="text-lg font-semibold text-gray-900 capitalize">
                {biometric.biometric_type === 'face'
                  ? 'Reconocimiento Facial'
                  : 'Huella Dactilar'}
              </h3>
            </div>
            <div className="flex gap-2">
              {biometric.is_primary && (
                <StatusBadge status="primary" label="Principal" size="sm" />
              )}
              <StatusBadge
                status={biometric.is_active ? 'active' : 'inactive'}
                label={biometric.is_active ? 'Activo' : 'Inactivo'}
                size="sm"
              />
            </div>
          </div>

          {biometric.thumbnail_url && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Vista Previa</h4>
              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <img
                  src={biometric.thumbnail_url}
                  alt="Biometric preview"
                  className="w-full h-auto max-h-64 object-contain bg-gray-100"
                />
              </div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-1">Tipo</h4>
              <p className="text-gray-900 capitalize">
                {biometric.biometric_type === 'face'
                  ? 'Reconocimiento Facial'
                  : 'Huella Dactilar'}
              </p>
            </div>

            {biometric.model_name && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">Modelo</h4>
                <p className="text-gray-900">{biometric.model_name}</p>
              </div>
            )}

            {biometric.quality_score !== null && biometric.quality_score !== undefined && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">
                  Puntuación de Calidad
                </h4>
                <p className="text-gray-900">{biometric.quality_score.toFixed(2)}</p>
              </div>
            )}

            {biometric.encryption_method && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-1">Encriptación</h4>
                <p className="text-gray-900">{biometric.encryption_method}</p>
              </div>
            )}

            {biometric.hash_checksum && (
              <div className="col-span-2">
                <h4 className="text-sm font-medium text-gray-700 mb-1">Hash Checksum</h4>
                <p className="text-gray-900 text-xs font-mono break-all">
                  {biometric.hash_checksum}
                </p>
              </div>
            )}
          </div>

          <div className="border-t border-gray-200 pt-4">
            <h4 className="text-sm font-medium text-gray-700 mb-3">Información del Sistema</h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500">Fecha de Creación</p>
                <p className="text-sm text-gray-900">{formatDate(biometric.created_at)}</p>
              </div>
              {biometric.updated_at && (
                <div>
                  <p className="text-xs text-gray-500">Última Actualización</p>
                  <p className="text-sm text-gray-900">{formatDate(biometric.updated_at)}</p>
                </div>
              )}
            </div>
          </div>

          {biometric.meta_info && Object.keys(biometric.meta_info).length > 0 && (
            <div className="border-t border-gray-200 pt-4">
              <h4 className="text-sm font-medium text-gray-700 mb-3">Metadatos</h4>
              <div className="bg-gray-50 rounded-lg p-3">
                <pre className="text-xs text-gray-800 overflow-x-auto">
                  {JSON.stringify(biometric.meta_info, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end px-6 py-4 bg-gray-50 rounded-b-lg border-t border-gray-200">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
