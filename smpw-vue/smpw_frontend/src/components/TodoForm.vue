<template>
 <h3 v-if="editing">Todo Detail</h3>
 <h3 v-else>Create Todo</h3>
    <div v-if="isLoading">
        Loading...
    </div>
    <form v-else @submit.prevent="onSave">
        <div class="row">
            <div class="col-6">
                <div class="form-group text-start">
                    <label for="title">Title:</label>
                    <div>
                        <input type="text" id="title" v-model="todoData.title">
                    </div>
                </div>
            </div>
            <div v-if="editing" class="col-6">
                <div class="form-group text-start">
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
            <div class="col-12">
                <div class="form-group text-start">
                    <label for="contents">Contents:</label>
                    <div>
                        <textarea class="form-control" type="text" id="contents" v-model="todoData.contents"></textarea>
                    </div>
                </div>
            </div>
        </div>    
        <br />
        <button type="submit" class="btn btn-primary" :disabled="!isTodoChanged">{{ editing ? 'Update' : 'Create' }}</button>
        <button type="button" class="btn btn-secondary" @click="moveToTodoListPage">Cancel</button>
    </form>
</template>

<script setup>

import { ref, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import _ from 'lodash'; 
import { useToast } from 'vue-toastification';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const todo_id = ref(route.params.todo_id);
const isLoading = ref(false);

const todoData = ref({
    subject: '',
    completed: false,
    contents:'' 
}); 
const originalTodoData = ref({});

const props = defineProps({
    editing: {
        type: Boolean,
        default: false
    }
})

const onSave = async () => {
    if (!todoData.value.title) {
        toast.error('Title is required');
        return;
    }


    let res = ''; 

    const data = { 
        title: todoData.value.title,
        completed: todoData.value.completed,
        contents: todoData.value.contents,
    }

    try {
        if (props.editing) {
            res = await axios.put(`http://localhost:4000/boards/todo_update/${todo_id.value}`, data);
            console.log(res.data);
            moveToTodoListPage();
        } else {
            res = await axios.post('http://localhost:4000/boards/todo_insert', data);
            console.log(res.data);
            moveToTodoListPage();
        }

        let message = "";
        if (props.editing) {
            message = "Todo updated successfully";
        } else {
            message = "Todo created successfully";
        }
        toast.success(message);
    } catch (error) {
        console.error('Error updating todo:', error);
        toast.error(error.response.data.message);
    }
}

const getTodoDetail = async () => {
    isLoading.value = true;
    try {
        const res = await axios.get(`http://localhost:4000/boards/todo_detail/${todo_id.value}`);
        todoData.value = {...res.data.todo_detail};
        originalTodoData.value = {...res.data.todo_detail};
        isLoading.value = false;
    } catch (error) {
        console.error('Error fetching todo detail:', error);
        isLoading.value = false;
    }
}

if (props.editing) {
    getTodoDetail();
}

const isTodoChanged = computed(() => {
    return !_.isEqual(todoData.value, originalTodoData.value);
});

const toggleCompleted = async () => {
    todoData.value.completed = !todoData.value.completed;
}

const moveToTodoListPage = () => {
    router.push({name: 'Todos'});
}

</script>

<style scoped>

</style>