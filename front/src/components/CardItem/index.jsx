import React, { useContext, useEffect, useState } from "react";
import ContentLoader from "react-content-loader";
import styles from "./styles.module.css";
import { Link } from "react-router-dom";
import { Navigation } from "../../App";

import { api, tokenManager } from "../../api";

export const CardItem = (props) => {
  const { setItemId } = useContext(Navigation);
  const { id, productId, name, price, url, isLoading = false, initialFav = false } = props;
  const [fav, setFav] = useState(initialFav);
  const isClient = tokenManager.getToken().type === "customer";
  const userId = tokenManager.getToken().id;
  
  const itemPath = isClient ? `/client/${userId}/item/${productId}` : `/customer/${userId}/item/${productId}`;

  useEffect(() => {
    setFav(initialFav);
  }, [initialFav]);

  async function handleOnChnageFavorite() {
    console.log("+++");
    try {
      if (fav) {
        await api.removeFromFavorites(productId);
      } else {
        await api.addToFavorites(productId);
      }
      setFav(!fav);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div>
      {isLoading ? (
        <div style={{ border: "1px solid gray" }}>
          <ContentLoader
            speed={2}
            width={170}
            height={220}
            viewBox="0 0 170 220"
            backgroundColor="#f3f3f3"
            foregroundColor="#ecebeb"
            {...props}
          >
            <rect x="20" y="18" rx="0" ry="0" width="130" height="130" />
            <rect x="20" y="160" rx="0" ry="0" width="73" height="17" />
            <rect x="20" y="180" rx="0" ry="0" width="54" height="17" />
          </ContentLoader>
        </div>
      ) : (
        <>
          <div className={styles.card}>
            <Link to={itemPath} onClick={() => {setItemId(productId);}}>
              <img alt="1" src={url} />
            </Link>
            <div className={styles.info}>
              <div>
                <h5>{name}</h5>
                <h5>{price} $</h5>
              </div>
              <div onClick={handleOnChnageFavorite}>
                {fav ? (
                  <svg width="18" height="17" viewBox="0 0 15 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M14.5849 3.22311C14.3615 2.7098 14.0394 2.24464 13.6365 1.85368C13.2333 1.46155 12.758 1.14993 12.2363 0.935761C11.6954 0.712803 11.1152 0.59868 10.5295 0.600018C9.70772 0.600018 8.90596 0.823295 8.20921 1.24504C8.04253 1.34593 7.88418 1.45674 7.73416 1.57748C7.58414 1.45674 7.42579 1.34593 7.2591 1.24504C6.56236 0.823295 5.7606 0.600018 4.93884 0.600018C4.3471 0.600018 3.7737 0.712483 3.23198 0.935761C2.70858 1.15077 2.23686 1.46005 1.83181 1.85368C1.42843 2.2442 1.10619 2.70947 0.883373 3.22311C0.65168 3.75732 0.533333 4.32461 0.533333 4.90844C0.533333 5.45919 0.646679 6.0331 0.871705 6.61693C1.06006 7.10483 1.33009 7.61092 1.67513 8.12198C2.22186 8.93074 2.97361 9.77423 3.90705 10.6293C5.4539 12.0467 6.98574 13.0258 7.05075 13.0655L7.44579 13.3169C7.62081 13.4277 7.84584 13.4277 8.02086 13.3169L8.4159 13.0655C8.48091 13.0242 10.0111 12.0467 11.5596 10.6293C12.493 9.77423 13.2448 8.93074 13.7915 8.12198C14.1366 7.61092 14.4083 7.10483 14.5949 6.61693C14.82 6.0331 14.9333 5.45919 14.9333 4.90844C14.935 4.32461 14.8166 3.75732 14.5849 3.22311Z"
                      fill="#FF8585"
                    />
                  </svg>
                ) : (
                  <svg width="18" height="17" viewBox="0 0 18 17" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                      d="M12.9537 0C14.3511 0 15.5249 0.47123 16.4751 1.41369C17.4253 2.35615 17.9004 3.5065 17.9004 4.86475C17.9004 5.53002 17.7607 6.20221 17.4812 6.88134C17.2017 7.56047 16.8943 8.16336 16.5589 8.69003C16.2235 9.2167 15.6576 9.89582 14.8611 10.7274C14.0646 11.559 13.3939 12.2312 12.8489 12.744C12.3039 13.2568 11.4305 14.0399 10.2288 15.0932L8.92924 16.2574L7.62968 15.1348C6.45588 14.0537 5.58951 13.2568 5.03056 12.744C4.4716 12.2312 3.79388 11.559 2.99737 10.7274C2.20087 9.89582 1.63493 9.2167 1.29956 8.69003C0.96419 8.16336 0.663754 7.56047 0.398252 6.88134C0.132751 6.20221 0 5.53002 0 4.86475C0 3.5065 0.475108 2.35615 1.42532 1.41369C2.37554 0.47123 3.53536 0 4.90479 0C6.52575 0 7.86723 0.623686 8.92924 1.87106C9.99124 0.623686 11.3327 0 12.9537 0ZM9.01308 13.8043C10.3825 12.5846 11.3816 11.6768 12.0105 11.0808C12.6393 10.4849 13.331 9.77109 14.0856 8.93951C14.8401 8.10792 15.3642 7.38029 15.6576 6.7566C15.9511 6.13292 16.0978 5.5023 16.0978 4.86475C16.0978 3.97773 15.7973 3.24317 15.1965 2.66106C14.5956 2.07895 13.848 1.7879 12.9537 1.7879C12.2829 1.7879 11.6471 1.98194 11.0463 2.37001C10.4454 2.75808 10.0192 3.25703 9.76766 3.86686H8.09081C7.86723 3.25703 7.455 2.75808 6.85413 2.37001C6.25326 1.98194 5.60348 1.7879 4.90479 1.7879C4.01047 1.7879 3.26986 2.07895 2.68296 2.66106C2.09606 3.24317 1.80262 3.97773 1.80262 4.86475C1.80262 5.5023 1.94235 6.13292 2.22183 6.7566C2.5013 7.38029 3.02532 8.10792 3.79388 8.93951C4.56243 9.77109 5.26112 10.4849 5.88994 11.0808C6.51876 11.6768 7.50391 12.5846 8.84539 13.8043L8.92924 13.8874L9.01308 13.8043Z"
                      fill="#9B9B9B"
                    />
                  </svg>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
