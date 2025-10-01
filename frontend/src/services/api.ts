import { Customer, CustomerFormData } from '../types/customer';
import { Biometric, BiometricFormData, BiometricUploadData } from '../types/biometric';

const BASE_URL = 'http://localhost:8000/api';

function getAuthHeaders(): HeadersInit {
  const token = sessionStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

function getAuthHeadersMultipart(): HeadersInit {
  const token = sessionStorage.getItem('token');
  return {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (response.status === 401) {
    sessionStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Session expired. Please login again.');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return handleResponse<{ access_token: string; token_type: string }>(response);
  },
};

export const customersAPI = {
  list: async (params?: {
    skip?: number;
    limit?: number;
    dni_type?: string;
    gender?: string;
    status?: string;
    search?: string;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.dni_type) queryParams.append('dni_type', params.dni_type);
    if (params?.gender) queryParams.append('gender', params.gender);
    if (params?.status) queryParams.append('status', params.status);
    if (params?.search) queryParams.append('search', params.search);

    const queryString = queryParams.toString();
    const url = queryString ? `${BASE_URL}/customers?${queryString}` : `${BASE_URL}/customers`;

    const response = await fetch(url, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Customer[]>(response);
  },

  get: async (customerId: string) => {
    const response = await fetch(`${BASE_URL}/customers/${customerId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Customer>(response);
  },

  create: async (customerData: CustomerFormData) => {
    const response = await fetch(`${BASE_URL}/customers`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(customerData),
    });
    return handleResponse<Customer>(response);
  },

  update: async (customerId: string, customerData: Partial<CustomerFormData>) => {
    const response = await fetch(`${BASE_URL}/customers/${customerId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(customerData),
    });
    return handleResponse<Customer>(response);
  },

  delete: async (customerId: string) => {
    const response = await fetch(`${BASE_URL}/customers/${customerId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse<{ message: string }>(response);
  },

  search: async (query: string) => {
    const response = await fetch(`${BASE_URL}/customers/search?q=${encodeURIComponent(query)}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Customer[]>(response);
  },
};

export const plansAPI = {
  list: async () => {
    const response = await fetch(`${BASE_URL}/plans`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },

  get: async (planId: string) => {
    const response = await fetch(`${BASE_URL}/plans/${planId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any>(response);
  },

  create: async (planData: any) => {
    const response = await fetch(`${BASE_URL}/plans`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(planData),
    });
    return handleResponse<any>(response);
  },

  update: async (planId: string, planData: any) => {
    const response = await fetch(`${BASE_URL}/plans/${planId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(planData),
    });
    return handleResponse<any>(response);
  },

  delete: async (planId: string) => {
    const response = await fetch(`${BASE_URL}/plans/${planId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse<{ message: string }>(response);
  },
};

export const subscriptionsAPI = {
  list: async () => {
    const response = await fetch(`${BASE_URL}/subscriptions`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },

  get: async (subscriptionId: string) => {
    const response = await fetch(`${BASE_URL}/subscriptions/${subscriptionId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any>(response);
  },

  create: async (subscriptionData: any) => {
    const response = await fetch(`${BASE_URL}/subscriptions`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(subscriptionData),
    });
    return handleResponse<any>(response);
  },

  update: async (subscriptionId: string, subscriptionData: any) => {
    const response = await fetch(`${BASE_URL}/subscriptions/${subscriptionId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(subscriptionData),
    });
    return handleResponse<any>(response);
  },

  getByCustomer: async (customerId: string) => {
    const response = await fetch(`${BASE_URL}/subscriptions/customer/${customerId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },
};

export const paymentsAPI = {
  list: async () => {
    const response = await fetch(`${BASE_URL}/payments`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },

  create: async (paymentData: any) => {
    const response = await fetch(`${BASE_URL}/payments`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(paymentData),
    });
    return handleResponse<any>(response);
  },

  getBySubscription: async (subscriptionId: string) => {
    const response = await fetch(`${BASE_URL}/payments/subscription/${subscriptionId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },
};

export const attendancesAPI = {
  list: async () => {
    const response = await fetch(`${BASE_URL}/attendances`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },

  checkIn: async (customerId: string) => {
    const response = await fetch(`${BASE_URL}/attendances/checkin/${customerId}`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    return handleResponse<any>(response);
  },

  getByCustomer: async (customerId: string) => {
    const response = await fetch(`${BASE_URL}/attendances/customer/${customerId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },

  getByDate: async (date: string) => {
    const response = await fetch(`${BASE_URL}/attendances/date/${date}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<any[]>(response);
  },
};

export const biometricsAPI = {
  list: async (customerId: string) => {
    const response = await fetch(`${BASE_URL}/biometrics/customer/${customerId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Biometric[]>(response);
  },

  get: async (biometricId: string) => {
    const response = await fetch(`${BASE_URL}/biometrics/${biometricId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Biometric>(response);
  },

  create: async (biometricData: BiometricFormData) => {
    const response = await fetch(`${BASE_URL}/biometrics`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(biometricData),
    });
    return handleResponse<Biometric>(response);
  },

  upload: async (uploadData: BiometricUploadData) => {
    const formData = new FormData();
    formData.append('customer_id', uploadData.customer_id);
    formData.append('biometric_type', uploadData.biometric_type);
    formData.append('file', uploadData.file);
    if (uploadData.quality_score !== undefined) {
      formData.append('quality_score', uploadData.quality_score.toString());
    }
    if (uploadData.is_primary !== undefined) {
      formData.append('is_primary', uploadData.is_primary.toString());
    }
    if (uploadData.metadata) {
      formData.append('metadata', JSON.stringify(uploadData.metadata));
    }

    const response = await fetch(`${BASE_URL}/biometrics/upload`, {
      method: 'POST',
      headers: getAuthHeadersMultipart(),
      body: formData,
    });
    return handleResponse<Biometric>(response);
  },

  update: async (biometricId: string, biometricData: Partial<BiometricFormData>) => {
    const response = await fetch(`${BASE_URL}/biometrics/${biometricId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(biometricData),
    });
    return handleResponse<Biometric>(response);
  },

  delete: async (biometricId: string) => {
    const response = await fetch(`${BASE_URL}/biometrics/${biometricId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    return handleResponse<{ message: string }>(response);
  },

  setPrimary: async (biometricId: string) => {
    const response = await fetch(`${BASE_URL}/biometrics/${biometricId}/primary`, {
      method: 'PUT',
      headers: getAuthHeaders(),
    });
    return handleResponse<Biometric>(response);
  },
};
