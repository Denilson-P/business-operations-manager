import { useState } from "react"

import { Interest } from "./pages/Interest"
import { Commissions } from "./pages/Commissions"
import { Inventory } from "./pages/Inventory"


type Page = "commissions" | "inventory" | "interest"


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

          <button
            className={
              currentPage === "interest" ? "active" : ""
            }
            onClick={() => setCurrentPage("interest")}
          >
            Interest
          </button>
        </nav>
      </header>

      {currentPage === "commissions" && <Commissions />}
      {currentPage === "inventory" && <Inventory />}
      {currentPage === "interest" && <Interest />}
    </>
  )
}

export default App