import { createPinia } from 'pinia'
import { persistedStatePlugin } from './plugins/persistedState'

const pinia = createPinia()
pinia.use(persistedStatePlugin)

export default pinia