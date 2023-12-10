import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";

import { Nav } from "../../components/Nav";
import { CardItem } from "../../components/CardItem";

export const ClientFav = () => {
  const [items, setItems] = useState([
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      name: "qweqweqwe",
      price: 123,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const items = await fetch(`http://localhost:3000/favoriteItems`).then((res) => res.json());
        setItems(items);
      } catch (error) {
        console.log(error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []); // возможно нужны зависимости для ререндера

  const renderItems = () => {
    return (isLoading ? [...Array(8)] : items).map((item, index) => {
      return <CardItem {...item} key={index} isLoading={isLoading} />;
    });
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <div className={styles.items}>{renderItems()}</div>
      </div>
    </div>
  );
};