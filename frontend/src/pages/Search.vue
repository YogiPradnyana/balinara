<template>
    <div class="px-[140px] mt-[78px] relative font-pr overflow-x-hidden text-neu-900">
  <div class="py-12">
    <h2 class="text-[28px] font-semibold mb-2">Search results for “Temple”</h2>
    <p class="text-neu-600 mb-10">Your adventure starts with places we found for you.</p>

    <div class="flex gap-8">
      <!-- Sidebar -->
      <div class="w-[240px] space-y-8">
        <div>
          <h3 class="font-semibold mb-2">Categories</h3>
          <ul class="space-y-2 text-neu-700">
            <li><input type="checkbox" class="mr-2">Beach</li>
            <li><input type="checkbox" class="mr-2">Mountain</li>
            <li><input type="checkbox" class="mr-2">Lake</li>
          </ul>
        </div>
        <div>
          <h3 class="font-semibold mb-2">Regency</h3>
          <ul class="space-y-2 text-neu-700">
            <li><input type="radio" name="regency" class="mr-2">Denpasar</li>
            <li><input type="radio" name="regency" class="mr-2">Badung</li>
            <li><input type="radio" name="regency" class="mr-2">Klungkung</li>
            <li><input type="radio" name="regency" class="mr-2">Bangli</li>
            <li><input type="radio" name="regency" class="mr-2">Tabanan</li>
            <li><input type="radio" name="regency" class="mr-2">Gianyar</li>
            <li><input type="radio" name="regency" class="mr-2">Buleleng</li>
            <li><input type="radio" name="regency" class="mr-2">Jembrana</li>
            <li><input type="radio" name="regency" class="mr-2">Karangasem</li>
          </ul>
        </div>
        <div>
          <h3 class="font-semibold mb-2">Rating</h3>
          <div class="flex gap-1">
            <span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span><span>⭐</span>
          </div>
        </div>
      </div>

      <!-- Search Result List -->
      <div class="flex-1 space-y-6">
        <!-- Card -->
        <div class="bg-white rounded-[20px] p-4 flex gap-4 shadow-sm" repeat="5">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Tirta_Empul_Tampak_Siring_Bali.jpg/640px-Tirta_Empul_Tampak_Siring_Bali.jpg" alt="Tirta Empul" class="rounded-[20px] w-[140px] h-[120px] object-cover">
          <div class="flex-1">
            <div class="flex justify-between">
              <h4 class="font-semibold text-[18px]">Tirta Empul Temple</h4>
              <div class="flex items-center gap-1 text-sm text-neu-500">
                <span>⭐</span>
                <span>4.8</span>
              </div>
            </div>
            <p class="text-neu-600 text-sm mt-1">Tampaksiring, Gianyar</p>
            <p class="text-neu-600 text-sm mt-2">Tirta Empul is a sacred temple in Bali with natural spring water baths, believed to have purifying and spiritual benefits.</p>
            <button class="mt-4 bg-pr-500 text-white px-4 py-2 rounded-full text-sm font-medium">View More</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>