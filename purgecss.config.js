module.exports = {
  // Scans index.html and 404.html in the root directory and all subdirectories
  content: ["./**/{index,404}.html"],

  // Custom extractor to handle Tailwind CSS class names (slashes, colons, dots, etc.)[cite: 1]
  defaultExtractor: (content) => content.match(/[\w-/:.]+(?<!:)/g) || [],

  // Keep CSS variables and keyframe animations[cite: 1]
  variables: true,
  keyframes: true
};
