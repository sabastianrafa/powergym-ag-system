import { useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import { CustomerRegistration } from './pages/CustomerRegistration';
import { CustomerDetail } from './pages/CustomerDetail';
import { CustomerEdit } from './pages/CustomerEdit';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const { isAuthenticated, isLoading } = useAuth();
  const currentPath = window.location.pathname;

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gym-red mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login />;
  }

  const renderPage = () => {
    if (currentPath === '/login') {
      window.location.href = '/';
      return null;
    }

    if (currentPath.startsWith('/customers/') && currentPath.endsWith('/edit')) {
      return <CustomerEdit />;
    }

    if (currentPath.startsWith('/customers/') && currentPath !== '/customers/new') {
      return <CustomerDetail />;
    }

    switch (currentPath) {
      case '/':
        return <Dashboard />;
      case '/customers':
        return <Customers />;
      case '/customers/new':
        return <CustomerRegistration />;
      case '/plans':
        return (
          <ProtectedRoute allowedRoles={['admin']}>
            <div className="text-center text-gray-600">Plans page - Coming soon</div>
          </ProtectedRoute>
        );
      case '/subscriptions':
        return (
          <ProtectedRoute allowedRoles={['admin']}>
            <div className="text-center text-gray-600">Subscriptions page - Coming soon</div>
          </ProtectedRoute>
        );
      case '/payments':
        return (
          <ProtectedRoute allowedRoles={['admin']}>
            <div className="text-center text-gray-600">Payments page - Coming soon</div>
          </ProtectedRoute>
        );
      case '/checkin':
        return <div className="text-center text-gray-600">Check-in page - Coming soon</div>;
      case '/attendances':
        return <div className="text-center text-gray-600">Attendances page - Coming soon</div>;
      default:
        return <Dashboard />;
    }
  };

  return <Layout>{renderPage()}</Layout>;
}

export default App;
