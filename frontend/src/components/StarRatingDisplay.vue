<script setup>
import Star from './icons/Star.vue'
import StarFilled from './icons/StarFilled.vue'

defineProps({
  rating: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 5,
  },
})
</script>
<template>
  <div class="flex gap-0.5 items-center">
    <template v-for="i in 5" :key="i">
      <StarFilled v-if="i <= rating" class="size-4.5 sm:size-5" />
      <Star v-else class="size-4.5 sm:size-5 text-[#FDB528]" />
    </template>
  </div>
</template>
