import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Calendar,
  Compass,
  FileText,
  DollarSign,
  TrendingUp,
  MapPin,
  Clock,
  Search,
} from 'lucide-react';

export function DashboardPage() {
  const { user } = useAuth();
  const [usersList, setUsersList] = useState<any[]>([]);
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8005';

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch(`${baseUrl}/user/users`, {
          credentials: 'include',
        });
        if (res.ok) {
          const data = await res.json();
          setUsersList(Array.isArray(data) ? data : [data]);
        }
      } catch (err) {
        console.error('Failed to fetch departures/users', err);
      }
    };

    fetchUsers();
  }, [baseUrl]);

  const welcomeName = user?.first_name || 'Agent';

  return (
    <div>
      {/* Welcome Section */}
      <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-[#0F172A]">
            Welcome Back, {welcomeName}!
          </h1>
          <p className="text-sm text-[#64748B] mt-1">
            Here is what is happening across your departures and bookings today.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <div className="relative">
            <Search className="w-4 h-4 text-[#94A3B8] absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search departures, PNR..."
              className="pl-9 pr-3 py-1.5 bg-white border border-[#E2E8F0] rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-[#74BDDA]/30 focus:border-[#74BDDA] w-56"
            />
          </div>
          <button className="px-3.5 py-1.5 bg-[#67b0ce] hover:bg-[#58a1be] text-white text-xs font-medium rounded-lg shadow-xs transition-all cursor-pointer">
            + New Booking
          </button>
        </div>
      </div>

      {/* 4 KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        {/* Card 1 */}
        <div className="bg-white p-5 rounded-2xl border border-[#E2E8F0] shadow-xs relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">
              Total Bookings
            </span>
            <div className="w-8 h-8 rounded-xl bg-[#eef7fa] flex items-center justify-center text-[#0891b2]">
              <Calendar className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#0F172A]">1,284</span>
            <span className="text-xs font-semibold text-emerald-600 flex items-center">
              <TrendingUp className="w-3 h-3 mr-0.5" /> +12.4%
            </span>
          </div>
          <div className="mt-2 h-1 w-full bg-[#F1F5F9] rounded-full overflow-hidden">
            <div className="h-full bg-[#74BDDA] rounded-full w-3/4" />
          </div>
        </div>

        {/* Card 2 */}
        <div className="bg-white p-5 rounded-2xl border border-[#E2E8F0] shadow-xs relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">
              Active Tours
            </span>
            <div className="w-8 h-8 rounded-xl bg-[#e6f9fa] flex items-center justify-center text-[#0891b2]">
              <Compass className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#0F172A]">48</span>
            <span className="text-xs font-semibold text-emerald-600 flex items-center">
              <TrendingUp className="w-3 h-3 mr-0.5" /> +4 new
            </span>
          </div>
          <div className="mt-2 h-1 w-full bg-[#F1F5F9] rounded-full overflow-hidden">
            <div className="h-full bg-[#95DEE4] rounded-full w-4/5" />
          </div>
        </div>

        {/* Card 3 */}
        <div className="bg-white p-5 rounded-2xl border border-[#E2E8F0] shadow-xs relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">
              Pending Manifests
            </span>
            <div className="w-8 h-8 rounded-xl bg-amber-50 flex items-center justify-center text-amber-600">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#0F172A]">6</span>
            <span className="text-xs font-medium text-amber-600">Due today</span>
          </div>
          <div className="mt-2 h-1 w-full bg-[#F1F5F9] rounded-full overflow-hidden">
            <div className="h-full bg-amber-400 rounded-full w-2/5" />
          </div>
        </div>

        {/* Card 4 */}
        <div className="bg-white p-5 rounded-2xl border border-[#E2E8F0] shadow-xs relative overflow-hidden">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-[#64748B] uppercase tracking-wider">
              Monthly Revenue
            </span>
            <div className="w-8 h-8 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600">
              <DollarSign className="w-4 h-4" />
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-[#0F172A]">$184,200</span>
            <span className="text-xs font-semibold text-emerald-600 flex items-center">
              <TrendingUp className="w-3 h-3 mr-0.5" /> +18.2%
            </span>
          </div>
          <div className="mt-2 h-1 w-full bg-[#F1F5F9] rounded-full overflow-hidden">
            <div className="h-full bg-emerald-500 rounded-full w-5/6" />
          </div>
        </div>
      </div>

      {/* Departure Activity Overview */}
      <div className="bg-white rounded-2xl border border-[#E2E8F0] shadow-xs overflow-hidden">
        <div className="p-5 border-b border-[#E2E8F0] flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-[#0F172A]">Upcoming Guaranteed Departures</h2>
            <p className="text-xs text-[#64748B]">Real-time manifest readiness and passenger capacity ({usersList.length} users registered)</p>
          </div>
          <span className="text-xs text-[#0891b2] font-semibold hover:underline cursor-pointer">
            View All Tours &rarr;
          </span>
        </div>

        <div className="divide-y divide-[#E2E8F0]">
          {[
            {
              id: 'DEP-8401',
              tour: 'Santorini & Cyclades Islands Discovery',
              destination: 'Santorini, Greece',
              date: 'Sep 02, 2026',
              seats: '24 / 24',
              status: 'Guaranteed',
              statusColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
            },
            {
              id: 'DEP-8402',
              tour: 'Dolomites Alpine Panorama & Lakes Trek',
              destination: 'South Tyrol, Italy',
              date: 'Sep 08, 2026',
              seats: '18 / 20',
              status: 'Guaranteed',
              statusColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
            },
            {
              id: 'DEP-8403',
              tour: 'Kyoto Heritage & Autumn Foliage',
              destination: 'Kyoto, Japan',
              date: 'Sep 15, 2026',
              seats: '12 / 16',
              status: 'Open',
              statusColor: 'bg-sky-50 text-sky-700 border-sky-200',
            },
          ].map((row) => (
            <div
              key={row.id}
              className="p-4 sm:px-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-[#EEF7FA]/40 transition-colors"
            >
              <div className="flex items-start sm:items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-[#EEF7FA] border border-[#74BDDA]/30 flex items-center justify-center text-[#0891b2] shrink-0">
                  <MapPin className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-medium text-[#64748B]">{row.id}</span>
                    <span className={`text-[11px] px-2 py-0.5 rounded-full border font-medium ${row.statusColor}`}>
                      {row.status}
                    </span>
                  </div>
                  <h3 className="text-sm font-semibold text-[#0F172A] mt-0.5">{row.tour}</h3>
                  <div className="flex items-center gap-3 text-xs text-[#64748B] mt-1">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-[#94A3B8]" />
                      {row.date}
                    </span>
                    <span>•</span>
                    <span>{row.destination}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between sm:justify-end gap-4 pl-13 sm:pl-0">
                <div className="text-right">
                  <p className="text-xs font-semibold text-[#0F172A]">{row.seats}</p>
                  <p className="text-[11px] text-[#64748B]">Capacity</p>
                </div>
                <button className="px-3 py-1.5 text-xs font-medium text-[#0891b2] hover:bg-[#EEF7FA] border border-[#74BDDA]/40 rounded-lg transition-colors cursor-pointer">
                  Manage Manifest
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
