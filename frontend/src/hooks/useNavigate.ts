export const useNavigate = () => {
  return (path: string) => {
    window.location.href = path;
  };
};

export const useParams = <T extends Record<string, string>>(): T => {
  const path = window.location.pathname;
  const segments = path.split('/').filter(Boolean);

  const params: any = {};

  if (segments[0] === 'customers' && segments[1] && segments[1] !== 'new') {
    params.id = segments[1];
  }

  return params as T;
};
