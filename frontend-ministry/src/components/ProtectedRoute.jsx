import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { token } = useAuth();
  const location = useLocation();

  // Si pas de token → Redirection immédiate vers /login
  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
    // replace empêche le bouton "Retour" de créer une boucle infinie
  }

  return children;
}