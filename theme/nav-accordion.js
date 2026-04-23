/**
 * Wiki.js sidebar — accordion behavior.
 * When a nav group opens, close sibling groups at the same level.
 * Injected via Wiki.js admin → Theme → HTML Head Injection.
 */
(function () {
  document.addEventListener('click', function (e) {
    var header = e.target.closest('.v-list-group__header');
    if (!header) return;
    var group = header.closest('.v-list-group');
    if (!group) return;
    var parent = group.parentElement;
    if (!parent) return;
    setTimeout(function () {
      var siblings = parent.querySelectorAll(':scope > .v-list-group--active');
      siblings.forEach(function (other) {
        if (other === group) return;
        var otherHeader = other.querySelector(':scope > .v-list-group__header');
        if (otherHeader) otherHeader.click();
      });
    }, 50);
  }, true);
})();
