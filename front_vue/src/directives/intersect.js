export default {
  mounted(el, binding) {
    const observer = new IntersectionObserver(binding.value, {
      threshold: 0.1
    });
    observer.observe(el);
  }
};
