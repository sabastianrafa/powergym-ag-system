import React, { useState, useEffect } from 'react';
import { Fingerprint, Plus, Eye, Trash2, CheckCircle } from 'lucide-react';
import { biometricsAPI } from '../../services/api';
import { Biometric } from '../../types/biometric';
import { StatusBadge } from '../ui/StatusBadge';
import { BiometricRegistrationModal } from './BiometricRegistrationModal';
import { BiometricDetailModal } from './BiometricDetailModal';
import { ConfirmDialog } from '../ui/ConfirmDialog';
import { useToast } from '../../hooks/useToast';

interface BiometricListProps {
  customerId: string;
}

export const BiometricList: React.FC<BiometricListProps> = ({ customerId }) => {
  const { success, error } = useToast();
  const [biometrics, setBiometrics] = useState<Biometric[]>([]);
  const [loading, setLoading] = useState(true);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [selectedBiometric, setSelectedBiometric] = useState<Biometric | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Biometric | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadBiometrics();
  }, [customerId]);

  const loadBiometrics = async () => {
    try {
      setLoading(true);
      const data = await biometricsAPI.list(customerId);
      setBiometrics(data);
    } catch (err) {
      error(err instanceof Error ? err.message : 'Error al cargar biométricos');
    } finally {
      setLoading(false);
    }
  };

  const handleSetPrimary = async (biometricId: string) => {
    try {
      await biometricsAPI.setPrimary(biometricId);
      success('Biométrico marcado como principal');
      loadBiometrics();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Error al actualizar biométrico');
    }
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    setIsDeleting(true);
    try {
      await biometricsAPI.delete(deleteTarget.id);
      success('Biométrico eliminado exitosamente');
      setDeleteTarget(null);
      loadBiometrics();
    } catch (err) {
      error(err instanceof Error ? err.message : 'Error al eliminar biométrico');
    } finally {
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <>
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-2">
            <Fingerprint className="text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Datos Biométricos</h3>
          </div>
          <button
            onClick={() => setShowRegisterModal(true)}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100"
          >
            <Plus className="w-4 h-4" />
            Registrar
          </button>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-sm text-gray-600">Cargando...</p>
          </div>
        ) : biometrics.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Fingerprint className="w-12 h-12 mx-auto mb-2 text-gray-400" />
            <p>No hay datos biométricos registrados</p>
          </div>
        ) : (
          <div className="space-y-3">
            {biometrics.map((biometric) => (
              <div
                key={biometric.id}
                className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <div className="flex-shrink-0">
                  <Fingerprint className="w-5 h-5 text-gray-600" />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <p className="text-sm font-medium text-gray-900 capitalize">
                      {biometric.biometric_type}
                    </p>
                    {biometric.is_primary && (
                      <StatusBadge status="primary" label="Principal" size="sm" />
                    )}
                    {biometric.is_active && (
                      <StatusBadge status="success" label="Activo" size="sm" />
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Registrado: {formatDate(biometric.created_at)}
                  </p>
                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => setSelectedBiometric(biometric)}
                    className="p-1.5 text-blue-600 hover:bg-blue-50 rounded"
                    title="Ver Detalles"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                  {!biometric.is_primary && (
                    <button
                      onClick={() => handleSetPrimary(biometric.id)}
                      className="p-1.5 text-green-600 hover:bg-green-50 rounded"
                      title="Marcar como Principal"
                    >
                      <CheckCircle className="w-4 h-4" />
                    </button>
                  )}
                  <button
                    onClick={() => setDeleteTarget(biometric)}
                    className="p-1.5 text-red-600 hover:bg-red-50 rounded"
                    title="Eliminar"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <BiometricRegistrationModal
        isOpen={showRegisterModal}
        onClose={() => setShowRegisterModal(false)}
        customerId={customerId}
        onSuccess={() => {
          setShowRegisterModal(false);
          loadBiometrics();
        }}
      />

      {selectedBiometric && (
        <BiometricDetailModal
          biometric={selectedBiometric}
          onClose={() => setSelectedBiometric(null)}
        />
      )}

      <ConfirmDialog
        isOpen={!!deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={handleDelete}
        title="Eliminar Dato Biométrico"
        message="¿Está seguro de que desea eliminar este dato biométrico? Esta acción no se puede deshacer."
        confirmText="Eliminar"
        cancelText="Cancelar"
        type="danger"
        isLoading={isDeleting}
      />
    </>
  );
};
