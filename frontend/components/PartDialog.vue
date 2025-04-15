<template>
  <v-dialog v-model="props.modelValue" max-width="600">
    <v-card>
      <v-card-title>
        <span v-if="props.part">Edit Part</span>
        <span v-else>Add Part</span>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="onSave">
          <v-text-field v-model="form.name" label="Part Name" required />
          <v-text-field v-model="form.stock" label="Stock" type="number" required />
        </v-form>
        <v-divider class="my-4" v-if="props.part" />
        <div v-if="props.part">
          <h3 class="subtitle-2 mb-2">Part History</h3>
          <v-list density="compact">
            <v-list-item v-for="(h, i) in history" :key="i">
              <v-list-item-title>
                Used on {{ h.date }} by {{ h.technician }} (Workorder #{{ h.workorder_id }})
              </v-list-item-title>
            </v-list-item>
            <v-list-item v-if="!history.length">
              <v-list-item-title>No history found.</v-list-item-title>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="onSave">Save</v-btn>
        <v-btn v-if="props.part" color="error" @click="onDelete">Delete</v-btn>
        <v-spacer />
        <v-btn text @click="() => emit('update:modelValue', false)">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps<{
  modelValue: boolean;
  part: any | null;
}>();
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
  (e: 'saved'): void;
  (e: 'deleted'): void;
}>();

const form = ref({
  name: '',
  stock: 0
});
const history = ref<any[]>([]);

watch(() => props.part, (val) => {
  if (val) {
    form.value = { ...val };
    // TODO: Fetch history from backend
    history.value = [];
  } else {
    form.value = { name: '', stock: 0 };
    history.value = [];
  }
}, { immediate: true });

function onSave() {
  // TODO: Save to backend
  emit('saved');
  emit('update:modelValue', false);
}
function onDelete() {
  // TODO: Delete from backend
  emit('deleted');
  emit('update:modelValue', false);
}
</script>
