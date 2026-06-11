# Frontend

React 18 + TypeScript + Vite frontend for the Job Application Tracker.

## Commands

```bash
npm install
npm run dev -- --host=127.0.0.1 --port=5173
npm run lint
npm run build
```

## Notes

- Auth access token is kept in Zustand memory.
- Refresh token is expected through the backend httpOnly cookie.
- Axios automatically refreshes access tokens on `401`.
- Tailwind colors are backed by CSS variables in `src/styles.css`.
- Main app routes are protected and redirect unauthenticated users to `/login`.
- Local API URL should be `VITE_API_URL=http://127.0.0.1:8051/api` when using the backend command above.
