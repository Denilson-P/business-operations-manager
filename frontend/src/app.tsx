import { useState } from "react"

import { Commissions } from "./pages/Commissions"
import { Inventory } from "./pages/Inventory"


type Page = "commissions" | "inventory"


function App() {
  const [currentPage, setCurrentPage] =
    useState<Page>("commissions")

  return (
    <>
      <header>
        <h1>Business Operations Manager</h1>

        <nav>
          <button
            className={
              currentPage === "commissions" ? "active" : ""
            }
            onClick={() => setCurrentPage("commissions")}
          >
            Commissions
          </button>

          <button
            className={
              currentPage === "inventory" ? "active" : ""
            }
            onClick={() => setCurrentPage("inventory")}
          >
            Inventory
          </button>
        </nav>
      </header>

      {currentPage === "commissions" && <Commissions />}
      {currentPage === "inventory" && <Inventory />}
    </>
  )
}

export default App