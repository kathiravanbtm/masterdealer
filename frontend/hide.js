function showSection(sectionId) {
  const sections = ['filter-section', 'dealer-list-section', 'upload-section', 'gstin-section', 'others-section'];
  sections.forEach(id => {
    document.getElementById(id).style.display = (id === sectionId) ? 'block' : 'none';
  });
}
