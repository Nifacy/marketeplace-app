import React, { createContext, useState } from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import { GetStarted } from "./pages/GetStarted";
import { Login } from "./pages/Login";
import { ClientReg } from "./pages/ClientReg";
import { CustomerReg } from "./pages/CustomerReg";
import { Client } from "./pages/Client/index";

export const Navigation = createContext(null);

function App() {
  const [isClient, setIsClient] = useState(false);
  const [clientId, setClientId] = useState();
  const [customerId, setCustomerId] = useState();

  return (
    <Navigation.Provider
      value={{
        isClient,
        setIsClient,
        clientId,
        setClientId,
        customerId,
        setCustomerId,
      }}
    >
      <Routes>
        <Route>
          <Route path="/" element={<GetStarted />} />
          <Route path="/login" element={<Login />} />
          <Route path="/client/registration" element={<ClientReg />} />
          <Route path="/customer/registration" element={<CustomerReg />} />
          <Route path="/client/:id" element={<Client />} />
          {/* <Route path="*" element={<NotFound />} /> */}
        </Route>
      </Routes>
    </Navigation.Provider>
  );
}

export default App;