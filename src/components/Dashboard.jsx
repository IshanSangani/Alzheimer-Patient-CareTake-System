import React from 'react';
import NavBar from './NavBar';

const patient = {
  name: "Eleanor Johnson",
  photo: "https://randomuser.me/api/portraits/women/44.jpg",
  lastUpdated: "Just now",
  address: "123 Maple Street, Portland, OR 97205",
  locationStatus: "At Home",
  safeZone: true,
  lastLocationUpdate: "09:15 PM",
};

const alerts = [
  {
    icon: 'warning',
    message: 'Possible fall detected in living room',
    level: 'High',
    time: '08:02 PM',
    details: 'View Details',
    mark: 'Mark as Read',
  },
  {
    icon: 'medication',
    message: 'Missed morning medication: Donepezil',
    level: 'Medium',
    time: '02:45 PM',
    details: 'View Details',
    mark: '',
  },
  {
    icon: 'favorite',
    message: 'Heart rate slightly elevated: 95 BPM',
    level: 'Low',
    time: '05:15 PM',
    details: 'View Details',
    mark: '',
  },
];

const device = {
  battery: 72,
  signal: 85,
  lastSynced: '09:15 PM',
  firmware: 'v2.1.0',
  status: 'Connected',
};

const Dashboard = () => (
  <>
    <NavBar />
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center gap-4 mb-6">
        <img src={patient.photo} alt={patient.name} className="w-14 h-14 rounded-full object-cover" />
        <div>
          <h1 className="text-2xl font-bold">{patient.name}'s Dashboard</h1>
          <div className="text-gray-600 text-sm">Last updated: {patient.lastUpdated}</div>
        </div>
        <div className="ml-auto">
          <button className="border rounded-lg px-4 py-2 text-sm font-medium flex items-center gap-2">
            <span className="material-icons text-base">calendar_today</span> Daily View
          </button>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Patient Location */}
        <div className="bg-white rounded-2xl shadow p-6 flex flex-col">
          <h2 className="font-semibold text-lg mb-2">Patient Location</h2>
          <div className="flex items-center gap-2 text-gray-700 mb-2">
            <span className="material-icons text-base">location_on</span>
            {patient.address}, <span className="font-medium">{patient.locationStatus}</span> {patient.safeZone && <span className="ml-1">Safe Zone</span>}
          </div>
          <div className="text-gray-500 text-sm mb-4">Last updated: {patient.lastLocationUpdate}</div>
          <div className="flex flex-col items-center justify-center flex-1">
            <span className="material-icons text-5xl mb-2">home</span>
            <div className="text-lg font-medium">Patient is at home</div>
          </div>
          <div className="flex justify-between mt-6 text-sm">
            <button className="hover:underline">View Detailed Map</button>
            <button className="hover:underline">Set Safe Zones</button>
          </div>
        </div>
        {/* Health Alerts */}
        <div className="bg-white rounded-2xl shadow p-6 flex flex-col">
          <h2 className="font-semibold text-lg mb-2">Health Alerts</h2>
          {alerts.map((alert, idx) => (
            <div key={idx} className="mb-4 border-b pb-2 last:border-b-0 last:pb-0">
              <div className="flex items-center gap-2">
                <span className="material-icons text-base">{alert.icon}</span>
                <span className="font-medium">{alert.message}</span>
                <span className="ml-auto text-xs font-semibold text-red-600">{alert.level}</span>
              </div>
              <div className="flex items-center text-xs text-gray-500 mt-1">
                {alert.time}
                <span className="ml-auto flex gap-4">
                  <button className="hover:underline">{alert.details}</button>
                  {alert.mark && <button className="hover:underline">{alert.mark}</button>}
                </span>
              </div>
            </div>
          ))}
          <div className="text-center mt-2">
            <button className="hover:underline text-sm">View All Alerts</button>
          </div>
        </div>
        {/* Device Status */}
        <div className="bg-white rounded-2xl shadow p-6 flex flex-col">
          <h2 className="font-semibold text-lg mb-2">Device Status</h2>
          <div className="flex items-center gap-6 mb-4">
            <div className="flex flex-col items-center">
              <span className="material-icons text-2xl">battery_full</span>
              <div className="text-lg font-bold">{device.battery}%</div>
              <div className="text-xs text-gray-500">OK</div>
            </div>
            <div className="flex flex-col items-center">
              <span className="material-icons text-2xl">wifi</span>
              <div className="text-lg font-bold">{device.signal}%</div>
              <div className="text-xs text-gray-500">Strong</div>
            </div>
          </div>
          <div className="text-sm text-gray-700 mb-2 flex items-center gap-2">
            <span className="material-icons text-base">schedule</span> Last Synced: {device.lastSynced}
          </div>
          <div className="text-sm text-gray-700 mb-2 flex items-center gap-2">
            <span className="material-icons text-base">memory</span> Firmware Version {device.firmware}
          </div>
          <div className="text-sm text-gray-700 mb-2 flex items-center gap-2">
            <span className="material-icons text-base">link</span> {device.status}
          </div>
          <div className="mt-4">
            <button className="hover:underline text-sm">Device Settings</button>
          </div>
        </div>
      </div>
    </div>
  </>
);

export default Dashboard;
