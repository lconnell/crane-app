<template>
  <v-dialog v-model="props.modelValue" max-width="600">
    <v-card>
      <v-card-title>
        <span v-if="workorder">Edit Workorder</span>
        <span v-else>Create Workorder</span>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="onSave">
          <v-text-field v-model="form.title" label="Title" required />
          <v-textarea v-model="form.description" label="Description" auto-grow />
          <v-text-field v-model="form.location" label="Location" required />
          <v-text-field v-model="form.technician" label="Technician" required />
          <v-select v-model="form.status" :items="statusOptions" label="Status" required />
          <v-text-field v-model="form.created_at" label="Created At" readonly />
          <v-text-field v-model="form.updated_at" label="Updated At" readonly />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="onSave">Save</v-btn>
        <v-btn v-if="workorder" color="error" @click="onDelete">Delete</v-btn>
        <v-spacer />
        <v-btn text @click="$emit('update:modelValue', false)">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
// Note: defineProps and defineEmits are compiler macros and do NOT need to be imported.

const props = defineProps({
  modelValue: Boolean,
  workorder: Object
});
const emit = defineEmits(['update:modelValue', 'saved', 'deleted']);

const statusOptions = ['in_progress', 'closed', 'completed'];

// Form fields must match backend
interface WorkorderForm {
  id: number | undefined;
  title: string;
  description: string;
  location: string;
  technician: string;
  status: string;
  created_at: string;
  updated_at: string;
}
// Always use WorkorderForm type for form. All assignments must include 'id'.
const form = ref<WorkorderForm>({
  id: undefined,
  title: '',
  description: '',
  location: '',
  technician: '',
  status: 'in_progress',
  created_at: '',
  updated_at: '',
});

watch(() => props.workorder, (val) => {
  if (val) {
    // Only copy fields that exist in our form
    form.value = {
      id: val.id,
      title: val.title || '',
      description: val.description || '',
      location: val.location || '',
      technician: val.technician || '',
      status: val.status || 'in_progress',
      created_at: val.created_at ? new Date(val.created_at).toLocaleString() : '',
      updated_at: val.updated_at ? new Date(val.updated_at).toLocaleString() : '',
    } as WorkorderForm; // Explicit type
  } else {
    form.value = {
      id: undefined,
      title: '',
      description: '',
      location: '',
      technician: '',
      status: 'in_progress',
      created_at: '',
      updated_at: '',
    } as WorkorderForm; // Explicit type
  }
}, { immediate: true });

async function onSave() {
  // Only send editable fields to parent
  try {
    // Type payload as Partial<WorkorderForm> so 'id' is allowed if present
    const payload: Partial<WorkorderForm> = {
      title: form.value.title,
      description: form.value.description,
      location: form.value.location,
      technician: form.value.technician,
      status: form.value.status,
    };
    // Always include id if present in form (robust for edit mode)
    if (form.value.id !== undefined) {
      payload.id = form.value.id;
    }
    await emit('saved', payload);
    emit('update:modelValue', false);
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('Failed to save workorder', err);
  }
}
async function onDelete() {
  // Call parent handler to delete workorder (must have id)
  try {
    if (props.workorder && props.workorder.id) {
      await emit('deleted', props.workorder.id);
    }
    emit('update:modelValue', false);
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error('Failed to delete workorder', err);
  }
}
</script>
