// persistedState.js
import { createPersistedState } from 'pinia-plugin-persistedstate'

export const persistedStatePlugin = createPersistedState({
  key: 'todo-app-state',
  paths: ['auth.token', 'auth.user'],
  storage: localStorage
})