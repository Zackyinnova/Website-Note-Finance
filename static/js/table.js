document.addEventListener("DOMContentLoaded", () => {
  const openBtn = document.querySelector(".button-add button");
  const modal = document.querySelector("#modalTransaksi");
  const closeBtn = modal.querySelector(".button-close");

  // Buka modal
  openBtn.addEventListener("click", () => {
    modal.classList.add("active");

    // fokus ke field pertama (opsional)
    const firstField = modal.querySelector("input, select, textarea");
    if (firstField) firstField.focus();
  });

  // Tutup modal (Cancel)
  closeBtn.addEventListener("click", () => {
    modal.classList.remove("active");

    // reset form (opsional)
    const form = modal.querySelector("form");
    if (form) form.reset();
  });

  // Klik area gelap untuk menutup (seperti modal modern)
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });

  // ESC untuk menutup
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") modal.classList.remove("active");
  });

  // button filter
  const filterTransaksi = document.getElementById("all-transaksi");
  const filterPemasukan = document.getElementById("pemasukan-transaksi");
  const filterPengeluaran = document.getElementById("pengeluaran-tranksaksi");
  const filterHigh = document.getElementById("Filter-high");
  const filterlow = document.getElementById("Filter-low");
  const filterNowHigh = document.getElementById("now-high");
  const filterNowLow = document.getElementById("now-low");

  // table data
  const tableAll = document.getElementById("table-data");
  const tableIncome = document.getElementById("table-dataincome");
  const tableExpense = document.getElementById("table-dataexpend")
  const tablehigh = document.getElementById("table-high")
  const tableLow = document.getElementById("table-low")
  const tableNowHigh = document.getElementById("table-nowhigh")
  const tableNowLow = document.getElementById("table-nowlow");


  function resetNavbarColors() {
    filterTransaksi.style.background = "#111C4A";
    filterPemasukan.style.background = "#111C4A";
    filterPengeluaran.style.background = "#111C4A";
  }

  filterTransaksi.addEventListener("click", () => {
    tableAll.style.display = "block";
    tableIncome.style.display = "none";
    tableExpense.style.display = "none";
    tablehigh.style.display ="none";
    tableLow.style.display ="none";
    tableNowHigh.style.display ="none";
    tableNowLow.style.display ="none";
    
    resetNavbarColors()
    filterTransaksi.style.background = "#1E3B6E";
  });

  filterPemasukan.addEventListener("click", () => {
    tableAll.style.display = "none";
    tableIncome.style.display = "block";
    tableExpense.style.display = "none";
    tablehigh.style.display ="none";
    tableLow.style.display ="none";
    tableNowHigh.style.display ="none";
    tableNowLow.style.display ="none";

    resetNavbarColors()
    filterPemasukan.style.background = "#1E3B6E";
  });

  filterPengeluaran.addEventListener("click", () => {
    tableAll.style.display = "none";
    tableIncome.style.display = "none";
    tableExpense.style.display = "block";
    tablehigh.style.display ="none";
    tableLow.style.display ="none";
    tableNowHigh.style.display ="none";
    tableNowLow.style.display ="none";

    resetNavbarColors()
    filterPengeluaran.style.background = "#1E3B6E";
  });

  filterHigh.addEventListener("click", () => {
    tableAll.style.display = "none";
    tableIncome.style.display = "none";
    tableExpense.style.display = "none";
    tablehigh.style.display ="block";
    tableLow.style.display ="none";
    tableNowHigh.style.display ="none";
    tableNowLow.style.display ="none";
  })

  filterlow.addEventListener("click", () => {
    tableAll.style.display = "none";
    tableIncome.style.display = "none";
    tableExpense.style.display = "none";
    tablehigh.style.display ="none";
    tableLow.style.display ="block";
    tableNowHigh.style.display ="none";
    tableNowLow.style.display ="none";
  })

  filterNowHigh.addEventListener("click", () => {
    tableAll.style.display = "none";
    tableIncome.style.display = "none";
    tableExpense.style.display = "none";
    tablehigh.style.display ="none";
    tableLow.style.display ="none";
    tableNowHigh.style.display ="block";
    tableNowLow.style.display ="none";
  })

  filterNowLow.addEventListener("click", () => {
    tableAll.style.display = "none";
    tableIncome.style.display = "none";
    tableExpense.style.display = "none";
    tablehigh.style.display ="none";
    tableLow.style.display ="none";
    tableNowHigh.style.display ="none";
    tableNowLow.style.display ="block";
  })


  const buttonFilter = document.getElementById("Filter-button");
  const overlayFilter = document.getElementById("overlay-filter");

  buttonFilter.addEventListener("mouseover", function (){
    overlayFilter.style.display = "block";
  });

  buttonFilter.addEventListener("mouseout", function (){
    overlayFilter.style.display = "none";
  });

  overlayFilter.addEventListener("mouseover", function(){
    overlayFilter.style.display = "block";
  });

  overlayFilter.addEventListener("mouseout", function(){
    overlayFilter.style.display = "none";
  })
  
});