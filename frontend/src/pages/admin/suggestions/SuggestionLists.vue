<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Edit from '@/components/icons/Edit.vue'
import Plus from '@/components/icons/Plus.vue'
import Search from '@/components/icons/Search.vue'
import Show from '@/components/icons/Show.vue'
import TrashCan from '@/components/icons/TrashCan.vue'
const tabs = ref([
  { id: 'all', label: 'All' },
  { id: 'pending', label: 'Pending' },
  { id: 'approved', label: 'Approved' },
  { id: 'rejected', label: 'Rejected' },
])

const activeTab = ref('pending')
const tabRefs = ref({})

const setActiveTab = (tabId) => {
  activeTab.value = tabId
}

const underlineStyle = computed(() => {
  const activeEl = tabRefs.value[activeTab.value]
  if (activeEl) {
    return {
      left: `${activeEl.offsetLeft}px`,
      width: `${activeEl.offsetWidth}px`,
    }
  }
  return { left: '0px', width: '0px' }
})

const updateUnderline = async () => {
  await nextTick()
  if (!tabRefs.value[activeTab.value]) {
    await nextTick()
  }
}

onMounted(() => {
  updateUnderline()
})

watch(activeTab, () => {
  updateUnderline()
})
</script>
<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Suggested Spot</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Reviews</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Suggested Spot</span>
      </div>
    </div>

    <div class="flex flex-col rounded-3xl border border-neu-100">
      <div class="flex flex-col p-4">
        <div class="flex justify-between sm:items-center flex-col sm:flex-row gap-4">
          <div
            class="border border-neu-100 gap-2 px-2.5 order-2 sm:order-1 py-2 flex items-center w-full sm:w-1/2 rounded-full"
          >
            <Search class="size-6" />
            <input
              type="text"
              class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
              placeholder="Search something..."
            />
          </div>
        </div>

        <div class="mt-4">
          <div class="relative flex overflow-x-auto">
            <!-- Tab List -->
            <div
              class="flex items-center space-x-2 sm:space-x-4 border-b border-gray-200"
              role="tablist"
              aria-label="Status Tabs"
            >
              <button
                v-for="tab in tabs"
                :key="tab.id"
                :ref="(el) => (tabRefs[tab.id] = el)"
                @click="setActiveTab(tab.id)"
                :class="[
                  'pb-2 sm:pb-3 px-2 cursor-pointer text-sm sm:text-base font-medium focus:outline-none transition-colors duration-300 ease-in-out',
                  activeTab === tab.id
                    ? 'text-pr-500 border-pr-600'
                    : 'text-neu-500 hover:text-neu-700',
                ]"
                role="tab"
                :aria-selected="activeTab === tab.id"
                :aria-controls="`tabpanel-${tab.id}`"
              >
                {{ tab.label }}
              </button>
            </div>

            <!-- Animated Underline -->
            <div
              class="absolute bottom-0 h-0.5 bg-pr-500 transition-all duration-300 ease-in-out"
              :style="underlineStyle"
            ></div>
          </div>

          <!-- Tab Panels (Konten untuk setiap tab) - Opsional -->
          <div class="mt-4">
            <div
              v-for="tab in tabs"
              :key="`panel-${tab.id}`"
              :id="`tabpanel-${tab.id}`"
              role="tabpanel"
              :aria-labelledby="tab.id"
            >
              <div v-if="activeTab === tab.id">
                <div class="mt-4 overflow-hidden border border-neu-100 rounded-2xl">
                  <div class="max-w-full overflow-x-auto">
                    <table class="min-w-180 w-full">
                      <thead class="bg-pr-500 text-xs text-white">
                        <tr>
                          <th class="p-4 text-start font-semibold w-12">NO</th>
                          <th class="p-4 text-start font-semibold">NAME</th>
                          <th class="p-4 text-start font-semibold">TRAVELER NAME</th>
                          <th class="p-4 text-start font-semibold">CATEGORY</th>
                          <th colspan="2" class="p-4 text-start font-semibold">ADDRESS</th>
                          <th class="p-4 text-start font-semibold">ACTION</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr class="text-sm text-neu-700 border-b border-neu-100">
                          <td class="p-4 text-neu-900">1</td>
                          <td class="p-4 text-neu-900 font-semibold">Tanah Lot</td>
                          <td class="p-4">Udin Surudin</td>
                          <td class="p-4">Beach</td>
                          <td colspan="2" class="p-4">
                            Beraban, Kecamatan Kediri, Kabupaten Tabanan
                          </td>
                          <td class="p-4 flex gap-3">
                            <RouterLink
                              :to="{ name: 'AdminSuggestionDetail', params: { id: 1 } }"
                              class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                            >
                              <Show class="size-5 text-neu-50" />
                            </RouterLink>
                            <button
                              type="button"
                              class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#B71A1A] bg-[#E02424]"
                            >
                              <TrashCan class="size-5 text-neu-50" />
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                <div class="flex justify-between items-center gap-3 flex-wrap mt-3">
                  <div class="text-sm text-neu-600">
                    Showing <span class="font-medium text-neu-900">1</span> to
                    <span class="font-medium text-neu-900">1</span> of
                    <span class="font-medium text-neu-900">10</span> Entries
                  </div>
                  <div class="flex items-center rounded-[8px] overflow-hidden">
                    <div
                      class="flex bg-neu-100 text-neu-300 gap-2 h-8 px-3 items-center font-semibold"
                    >
                      <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
                    </div>
                    <div
                      class="flex bg-neu-100 gap-2 h-8 px-3 cursor-pointer items-center font-semibold"
                    >
                      Next<ArrowRight2Bold class="size-4" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
