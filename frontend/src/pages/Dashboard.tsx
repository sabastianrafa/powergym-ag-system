import { useAuth } from '../context/AuthContext';
import { Users, Calendar, DollarSign, TrendingUp } from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gym-dark mb-2">
          Welcome back, {user?.name || user?.email}
        </h1>
        <p className="text-gray-600">Here's what's happening in your gym today</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-blue-100 p-3 rounded-lg">
              <Users className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-gym-dark mb-1">0</h3>
          <p className="text-sm text-gray-600">Active Members</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-green-100 p-3 rounded-lg">
              <Calendar className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-gym-dark mb-1">0</h3>
          <p className="text-sm text-gray-600">Today's Check-ins</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-yellow-100 p-3 rounded-lg">
              <DollarSign className="w-6 h-6 text-yellow-600" />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-gym-dark mb-1">$0</h3>
          <p className="text-sm text-gray-600">Monthly Revenue</p>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <div className="bg-gym-red bg-opacity-10 p-3 rounded-lg">
              <TrendingUp className="w-6 h-6 text-gym-red" />
            </div>
          </div>
          <h3 className="text-2xl font-bold text-gym-dark mb-1">0</h3>
          <p className="text-sm text-gray-600">Expiring Soon</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
        <h2 className="text-xl font-bold text-gym-dark mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/customers"
            className="p-4 border-2 border-gray-200 rounded-lg hover:border-gym-red hover:bg-red-50 transition-colors"
          >
            <Users className="w-8 h-8 text-gym-red mb-2" />
            <h3 className="font-semibold text-gym-dark">Manage Customers</h3>
            <p className="text-sm text-gray-600 mt-1">Add or edit customer profiles</p>
          </a>

          <a
            href="/checkin"
            className="p-4 border-2 border-gray-200 rounded-lg hover:border-gym-blue hover:bg-blue-50 transition-colors"
          >
            <Calendar className="w-8 h-8 text-gym-blue mb-2" />
            <h3 className="font-semibold text-gym-dark">Check-In Member</h3>
            <p className="text-sm text-gray-600 mt-1">Register gym attendance</p>
          </a>

          {user?.role === 'admin' && (
            <a
              href="/payments"
              className="p-4 border-2 border-gray-200 rounded-lg hover:border-green-600 hover:bg-green-50 transition-colors"
            >
              <DollarSign className="w-8 h-8 text-green-600 mb-2" />
              <h3 className="font-semibold text-gym-dark">Process Payment</h3>
              <p className="text-sm text-gray-600 mt-1">Record membership payments</p>
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
