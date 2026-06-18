import { ref, watch, type Ref } from 'vue'

export function useDebouncedRef(source: Ref<string>, delayMs = 250) {
  const debounced = ref(source.value)
  let timer: ReturnType<typeof setTimeout> | null = null

  watch(
    source,
    (value) => {
      if (timer) window.clearTimeout(timer)
      timer = window.setTimeout(() => {
        debounced.value = value
        timer = null
      }, delayMs)
    },
    { immediate: true }
  )

  return debounced
}
