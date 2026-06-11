import { Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "./components/layout/AppShell";
import { useAuthStore } from "./store/auth";
import { ApplicationDetail } from "./pages/ApplicationDetail";
import { Applications } from "./pages/Applications";
import { Contacts } from "./pages/Contacts";
import { Dashboard } from "./pages/Dashboard";
import { Resumes } from "./pages/Resumes";
import { Settings } from "./pages/Settings";
import { Stats } from "./pages/Stats";
import { ForgotPassword } from "./pages/auth/ForgotPassword";
import { Login } from "./pages/auth/Login";
import { Register } from "./pages/auth/Register";
import { ResetPassword } from "./pages/auth/ResetPassword";

function ProtectedRoute(): JSX.Element {
  const token = useAuthStore((state) => state.accessToken);
  return token ? <AppShell /> : <Navigate replace to="/login" />;
}

export default function App(): JSX.Element {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/applications" element={<Applications />} />
        <Route path="/applications/:id" element={<ApplicationDetail />} />
        <Route path="/stats" element={<Stats />} />
        <Route path="/contacts" element={<Contacts />} />
        <Route path="/resumes" element={<Resumes />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

