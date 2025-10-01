import React, { useState, FormEvent } from 'react';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { DatePicker } from '../ui/DatePicker';
import { CustomerFormData } from '../../types/customer';

interface CustomerFormProps {
  initialData?: Partial<CustomerFormData>;
  onSubmit: (data: CustomerFormData) => Promise<void>;
  onCancel: () => void;
  isEdit?: boolean;
}

interface FormErrors {
  [key: string]: string;
}

const DNI_TYPE_OPTIONS = [
  { value: 'CC', label: 'Cédula de Ciudadanía' },
  { value: 'TI', label: 'Tarjeta de Identidad' },
  { value: 'CE', label: 'Cédula de Extranjería' },
  { value: 'PP', label: 'Pasaporte' },
];

const GENDER_OPTIONS = [
  { value: 'M', label: 'Masculino' },
  { value: 'F', label: 'Femenino' },
  { value: 'O', label: 'Otro' },
];

export const CustomerForm: React.FC<CustomerFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isEdit = false,
}) => {
  const [formData, setFormData] = useState<CustomerFormData>({
    dni_type: initialData?.dni_type || '',
    dni_number: initialData?.dni_number || '',
    first_name: initialData?.first_name || '',
    middle_name: initialData?.middle_name || '',
    last_name: initialData?.last_name || '',
    second_last_name: initialData?.second_last_name || '',
    birth_date: initialData?.birth_date || '',
    gender: initialData?.gender || '',
    phone: initialData?.phone || '',
    alternative_phone: initialData?.alternative_phone || '',
    address: initialData?.address || '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.dni_type) {
      newErrors.dni_type = 'Tipo de documento es requerido';
    }

    if (!formData.dni_number.trim()) {
      newErrors.dni_number = 'Número de documento es requerido';
    } else if (!/^\d+$/.test(formData.dni_number.trim())) {
      newErrors.dni_number = 'Número de documento debe contener solo números';
    }

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'Primer nombre es requerido';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Primer apellido es requerido';
    }

    if (!formData.birth_date) {
      newErrors.birth_date = 'Fecha de nacimiento es requerida';
    } else {
      const birthDate = new Date(formData.birth_date);
      const today = new Date();
      const age = today.getFullYear() - birthDate.getFullYear();
      if (age < 0 || age > 120) {
        newErrors.birth_date = 'Fecha de nacimiento no válida';
      }
    }

    if (!formData.gender) {
      newErrors.gender = 'Género es requerido';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Teléfono es requerido';
    } else if (!/^\d{7,15}$/.test(formData.phone.trim())) {
      newErrors.phone = 'Teléfono debe tener entre 7 y 15 dígitos';
    }

    if (formData.alternative_phone && !/^\d{7,15}$/.test(formData.alternative_phone.trim())) {
      newErrors.alternative_phone = 'Teléfono alternativo debe tener entre 7 y 15 dígitos';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (field: keyof CustomerFormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Información de Identificación
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Tipo de Documento"
            options={DNI_TYPE_OPTIONS}
            value={formData.dni_type}
            onChange={(e) => handleChange('dni_type', e.target.value)}
            error={errors.dni_type}
            required
          />
          <Input
            label="Número de Documento"
            type="text"
            value={formData.dni_number}
            onChange={(e) => handleChange('dni_number', e.target.value)}
            error={errors.dni_number}
            disabled={isEdit}
            required
          />
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Información Personal
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Primer Nombre"
            type="text"
            value={formData.first_name}
            onChange={(e) => handleChange('first_name', e.target.value)}
            error={errors.first_name}
            required
          />
          <Input
            label="Segundo Nombre"
            type="text"
            value={formData.middle_name}
            onChange={(e) => handleChange('middle_name', e.target.value)}
          />
          <Input
            label="Primer Apellido"
            type="text"
            value={formData.last_name}
            onChange={(e) => handleChange('last_name', e.target.value)}
            error={errors.last_name}
            required
          />
          <Input
            label="Segundo Apellido"
            type="text"
            value={formData.second_last_name}
            onChange={(e) => handleChange('second_last_name', e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Información Demográfica
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DatePicker
            label="Fecha de Nacimiento"
            value={formData.birth_date}
            onChange={(e) => handleChange('birth_date', e.target.value)}
            error={errors.birth_date}
            max={new Date().toISOString().split('T')[0]}
            required
          />
          <Select
            label="Género"
            options={GENDER_OPTIONS}
            value={formData.gender}
            onChange={(e) => handleChange('gender', e.target.value)}
            error={errors.gender}
            required
          />
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Información de Contacto
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Teléfono Principal"
            type="tel"
            value={formData.phone}
            onChange={(e) => handleChange('phone', e.target.value)}
            error={errors.phone}
            required
          />
          <Input
            label="Teléfono Alternativo"
            type="tel"
            value={formData.alternative_phone}
            onChange={(e) => handleChange('alternative_phone', e.target.value)}
            error={errors.alternative_phone}
          />
        </div>
        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Dirección
          </label>
          <textarea
            value={formData.address}
            onChange={(e) => handleChange('address', e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-200 focus:border-blue-500"
          />
        </div>
      </div>

      <div className="flex gap-3 justify-end">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-6 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Guardando...' : isEdit ? 'Actualizar' : 'Registrar'}
        </button>
      </div>
    </form>
  );
};
