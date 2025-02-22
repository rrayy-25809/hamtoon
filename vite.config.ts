import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: '/index.html',
        login: '/login.html',
        signup: '/signup.html',
        mypage: '/mypage.html'
      }
    }
  }
});