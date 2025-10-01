import React, { useState } from 'react';
import { useNavigate } from '../hooks/useNavigate';
import { ArrowLeft } from 'lucide-react';
import { CustomerForm } from '../components/customers/CustomerForm';
import { customersAPI } from '../services/api';
import { CustomerFormData } from '../types/customer';
import { ToastContainer } from '../components/ui/Toast';
import { useToast } from '../hooks/useToast';

export const CustomerRegistration: React.FC = () => {
  const navigate = useNavigate();
  const { toasts, removeToast, success, error } = useToast();
  const [isNavigating, setIsNavigating] = useState(false);

  const handleSubmit = async (data: CustomerFormData) => {
    try {
      const customer = await customersAPI.create(data);
      success('Cliente registrado exitosamente');
      setIsNavigating(true);
      setTimeout(() => {
        navigate(`/customers/${customer.id}`);
      }, 1000);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Error al registrar cliente';
      error(message);
      throw err;
    }
  };

  const handleCancel = () => {
    navigate('/customers');
  };

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
            Volver a Clientes
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Registrar Nuevo Cliente</h1>
          <p className="text-gray-600 mt-2">
            Complete todos los campos requeridos para registrar un nuevo cliente
          </p>
        </div>

        <CustomerForm onSubmit={handleSubmit} onCancel={handleCancel} />
      </div>
    </div>
  );
};
