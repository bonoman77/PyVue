<template>
    <h3>Todo Detail</h3>
    <div v-if="isLoading">
        Loading...
    </div>
    <form v-else @submit.prevent="onSave">
        <div class="row">
            <div class="col-6">
                <div class="form-group">
                    <label for="title">Title:</label>
                    <div>
                        <input type="text" id="title" v-model="todoData.title">
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div class="form-group">
                    <label for="completed">Status:</label>
                    <div>
                        <button type="button" id="completed" class="btn btn-sm" :class="todoData.completed ? 'btn-danger' : 'btn-success'"
                        @click="toggleCompleted"
                        >
                            {{ todoData.completed ? 'Completed' : 'Incompleted' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>    

        <button type="submit" class="btn btn-primary" :disabled="!isTodoChanged">Update</button>
        <button type="button" class="btn btn-secondary" @click="moveToTodoListPage">Cancel</button>
    </form>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeMount } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import _ from 'lodash'; 
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const todo_id = ref(route.params.todo_id);
const isLoading = ref(true);

const todoData = ref({});
const originalTodoData = ref({});

const getTodoDetail = async () => {
    try {
        const res = await axios.get(`http://localhost:4000/boards/todo_detail/${todo_id.value}`);
        todoData.value = {...res.data.todo_detail};
        originalTodoData.value = {...res.data.todo_detail};
        isLoading.value = false;
    } catch (error) {
        console.error('Error fetching todo detail:', error);
    }
}

const isTodoChanged = computed(() => {
    return !_.isEqual(todoData.value, originalTodoData.value);
});

getTodoDetail();

const toggleCompleted = async () => {
    todoData.value.completed = !todoData.value.completed;
}

const moveToTodoListPage = () => {
    router.push({name: 'Todos'});
}

const onSave = async () => {
    try {
        const res = await axios.put(`http://localhost:4000/boards/todo_update/${todo_id.value}`, {
            title: todoData.value.title,
            completed: todoData.value.completed,
        });
        console.log(res.data);
        toast.success('Todo updated successfully');
        moveToTodoListPage();
    } catch (error) {
        console.error('Error updating todo:', error);
        toast.error('Error updating todo');
    }
}

</script>

<style scoped>


</style>
