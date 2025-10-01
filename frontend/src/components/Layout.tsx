import { ReactNode, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Dumbbell,
  Users,
  CreditCard,
  Calendar,
  DollarSign,
  BarChart3,
  LogOut,
  Menu,
  X,
  UserCheck,
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
}

interface NavItem {
  name: string;
  path: string;
  icon: any;
  roles: ('admin' | 'employee')[];
}

const navigation: NavItem[] = [
  { name: 'Dashboard', path: '/', icon: BarChart3, roles: ['admin', 'employee'] },
  { name: 'Customers', path: '/customers', icon: Users, roles: ['admin', 'employee'] },
  { name: 'Plans', path: '/plans', icon: CreditCard, roles: ['admin'] },
  { name: 'Subscriptions', path: '/subscriptions', icon: Calendar, roles: ['admin'] },
  { name: 'Payments', path: '/payments', icon: DollarSign, roles: ['admin'] },
  { name: 'Check-In', path: '/checkin', icon: UserCheck, roles: ['admin', 'employee'] },
  { name: 'Attendances', path: '/attendances', icon: Calendar, roles: ['admin', 'employee'] },
];

export default function Layout({ children }: LayoutProps) {
  const { user, logout } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const currentPath = window.location.pathname;

  const filteredNavigation = navigation.filter((item) =>
    user ? item.roles.includes(user.role) : false
  );

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="lg:hidden fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-30">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-2">
            <Dumbbell className="w-6 h-6 text-gym-red" />
            <span className="font-bold text-gym-dark">Gym Manager</span>
          </div>
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 rounded-lg hover:bg-gray-100"
          >
            {isSidebarOpen ? (
              <X className="w-6 h-6 text-gym-dark" />
            ) : (
              <Menu className="w-6 h-6 text-gym-dark" />
            )}
          </button>
        </div>
      </div>

      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-white border-r border-gray-200 z-40 transform transition-transform duration-300 ease-in-out ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0`}
      >
        <div className="flex flex-col h-full">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center gap-3">
              <div className="bg-gym-red p-2 rounded-lg">
                <Dumbbell className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="font-bold text-gym-dark text-lg">Gym Manager</h1>
                <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
              </div>
            </div>
          </div>

          <nav className="flex-1 p-4 overflow-y-auto">
            <ul className="space-y-1">
              {filteredNavigation.map((item) => {
                const Icon = item.icon;
                const isActive = currentPath === item.path;
                return (
                  <li key={item.path}>
                    <a
                      href={item.path}
                      className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-gym-red text-white'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span className="font-medium">{item.name}</span>
                    </a>
                  </li>
                );
              })}
            </ul>
          </nav>

          <div className="p-4 border-t border-gray-200">
            <div className="mb-3 px-4">
              <p className="text-sm font-semibold text-gym-dark">{user?.name || user?.email}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full px-4 py-3 text-gray-700 hover:bg-red-50 hover:text-gym-red rounded-lg transition-colors"
            >
              <LogOut className="w-5 h-5" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </aside>

      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      <main className="lg:ml-64 pt-16 lg:pt-0">
        <div className="p-6 lg:p-8">{children}</div>
      </main>
    </div>
  );
}
