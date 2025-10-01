import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from '../hooks/useNavigate';
import { ArrowLeft, CreditCard as Edit, Trash2, User, Phone, Calendar, MapPin, FileText } from 'lucide-react';
import { customersAPI } from '../services/api';
import { Customer } from '../types/customer';
import { StatusBadge } from '../components/ui/StatusBadge';
import { ConfirmDialog } from '../components/ui/ConfirmDialog';
import { ToastContainer } from '../components/ui/Toast';
import { useToast } from '../hooks/useToast';
import { BiometricList } from '../components/biometrics/BiometricList';

export const CustomerDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toasts, removeToast, success, error } = useToast();

  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadCustomer();
  }, [id]);

  const loadCustomer = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const data = await customersAPI.get(id);
      setCustomer(data);
    } catch (err) {
      error(err instanceof Error ? err.message : 'Error al cargar cliente');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    setIsDeleting(true);
    try {
      await customersAPI.delete(id);
      success('Cliente eliminado exitosamente');
      setTimeout(() => {
        navigate('/customers');
      }, 1000);
    } catch (err) {
      error(err instanceof Error ? err.message : 'Error al eliminar cliente');
      setIsDeleting(false);
      setShowDeleteDialog(false);
    }
  };

  const getFullName = () => {
    if (!customer) return '';
    const parts = [
      customer.first_name,
      customer.middle_name,
      customer.last_name,
      customer.second_last_name,
    ].filter(Boolean);
    return parts.join(' ');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  if (!customer) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Cliente no encontrado</p>
          <button
            onClick={() => navigate('/customers')}
            className="mt-4 text-blue-600 hover:text-blue-800"
          >
            Volver a Clientes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <ToastContainer toasts={toasts} onRemove={removeToast} />
      <ConfirmDialog
        isOpen={showDeleteDialog}
        onClose={() => setShowDeleteDialog(false)}
        onConfirm={handleDelete}
        title="Eliminar Cliente"
        message={`¿Está seguro de que desea eliminar a ${getFullName()}? Esta acción no se puede deshacer.`}
        confirmText="Eliminar"
        cancelText="Cancelar"
        type="danger"
        isLoading={isDeleting}
      />

      <div className="max-w-6xl mx-auto px-4">
        <div className="mb-6">
          <button
            onClick={() => navigate('/customers')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            Volver a Clientes
          </button>

          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{getFullName()}</h1>
              <div className="flex items-center gap-3 mt-2">
                <StatusBadge status={customer.status === 'active' ? 'active' : 'inactive'} />
                <span className="text-gray-600">
                  {customer.dni_type} {customer.dni_number}
                </span>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => navigate(`/customers/${id}/edit`)}
                className="flex items-center gap-2 px-4 py-2 text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100"
              >
                <Edit className="w-4 h-4" />
                Editar
              </button>
              <button
                onClick={() => setShowDeleteDialog(true)}
                className="flex items-center gap-2 px-4 py-2 text-red-600 bg-red-50 rounded-lg hover:bg-red-100"
              >
                <Trash2 className="w-4 h-4" />
                Eliminar
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <User className="text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Información Personal</h2>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Primer Nombre</p>
                  <p className="text-gray-900 font-medium">{customer.first_name}</p>
                </div>
                {customer.middle_name && (
                  <div>
                    <p className="text-sm text-gray-500">Segundo Nombre</p>
                    <p className="text-gray-900 font-medium">{customer.middle_name}</p>
                  </div>
                )}
                <div>
                  <p className="text-sm text-gray-500">Primer Apellido</p>
                  <p className="text-gray-900 font-medium">{customer.last_name}</p>
                </div>
                {customer.second_last_name && (
                  <div>
                    <p className="text-sm text-gray-500">Segundo Apellido</p>
                    <p className="text-gray-900 font-medium">{customer.second_last_name}</p>
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <FileText className="text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Identificación</h2>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Tipo de Documento</p>
                  <p className="text-gray-900 font-medium">{customer.dni_type}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Número de Documento</p>
                  <p className="text-gray-900 font-medium">{customer.dni_number}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <Calendar className="text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Demografía</h2>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Fecha de Nacimiento</p>
                  <p className="text-gray-900 font-medium">{formatDate(customer.birth_date)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Género</p>
                  <p className="text-gray-900 font-medium">{customer.gender}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <div className="flex items-center gap-2 mb-4">
                <Phone className="text-blue-600" />
                <h2 className="text-xl font-semibold text-gray-900">Contacto</h2>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Teléfono Principal</p>
                  <a
                    href={`tel:${customer.phone}`}
                    className="text-blue-600 hover:underline font-medium"
                  >
                    {customer.phone}
                  </a>
                </div>
                {customer.alternative_phone && (
                  <div>
                    <p className="text-sm text-gray-500">Teléfono Alternativo</p>
                    <a
                      href={`tel:${customer.alternative_phone}`}
                      className="text-blue-600 hover:underline font-medium"
                    >
                      {customer.alternative_phone}
                    </a>
                  </div>
                )}
              </div>
            </div>

            {customer.address && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <div className="flex items-center gap-2 mb-4">
                  <MapPin className="text-blue-600" />
                  <h2 className="text-xl font-semibold text-gray-900">Dirección</h2>
                </div>
                <p className="text-gray-900">{customer.address}</p>
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Información del Sistema</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-500">Estado</p>
                  <StatusBadge
                    status={customer.status === 'active' ? 'active' : 'inactive'}
                    size="sm"
                  />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Fecha de Registro</p>
                  <p className="text-sm text-gray-900">{formatDate(customer.created_at)}</p>
                </div>
                {customer.updated_at && (
                  <div>
                    <p className="text-sm text-gray-500">Última Actualización</p>
                    <p className="text-sm text-gray-900">{formatDate(customer.updated_at)}</p>
                  </div>
                )}
              </div>
            </div>

            {id && <BiometricList customerId={id} />}
          </div>
        </div>
      </div>
    </div>
  );
};
