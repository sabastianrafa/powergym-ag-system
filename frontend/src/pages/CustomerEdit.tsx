import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from '../hooks/useNavigate';
import { ArrowLeft } from 'lucide-react';
import { CustomerForm } from '../components/customers/CustomerForm';
import { customersAPI } from '../services/api';
import { CustomerFormData, Customer } from '../types/customer';
import { ToastContainer } from '../components/ui/Toast';
import { useToast } from '../hooks/useToast';

export const CustomerEdit: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toasts, removeToast, success, error } = useToast();

  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [isNavigating, setIsNavigating] = useState(false);

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

  const handleSubmit = async (data: CustomerFormData) => {
    if (!id) return;
    try {
      await customersAPI.update(id, data);
      success('Cliente actualizado exitosamente');
      setIsNavigating(true);
      setTimeout(() => {
        navigate(`/customers/${id}`);
      }, 1000);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al actualizar cliente';
      error(message);
      throw err;
    }
  };

  const handleCancel = () => {
    navigate(`/customers/${id}`);
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
      <div className="max-w-4xl mx-auto px-4">
        <div className="mb-6">
          <button
            onClick={handleCancel}
            disabled={isNavigating}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            Volver a Detalles
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Editar Cliente</h1>
          <p className="text-gray-600 mt-2">
            Actualice la información del cliente
          </p>
        </div>

        <CustomerForm
          initialData={customer}
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          isEdit={true}
        />
      </div>
    </div>
  );
};
