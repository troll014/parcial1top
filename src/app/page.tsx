"use client";

import React, { useEffect, useState } from "react";
import { collection, getDocs, query, orderBy } from "firebase/firestore";
import { db } from "../lib/firebase";
import { Card, CardContent, CardHeader } from "../components/ui/card";
import { Skeleton } from "../components/ui/skeleton";
import styles from "../styles/home.module.css";

interface NewsArticle {
  id: string;
  title: string;
  content: string;
  publishedAt: Date;
}

export default function HomePage() {
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNews() {
      setLoading(true);
      try {
        const q = query(collection(db, "news"), orderBy("publishedAt", "desc"));
        const querySnapshot = await getDocs(q);
        const newsData: NewsArticle[] = [];
        querySnapshot.forEach((doc) => {
          const data = doc.data();
          newsData.push({
            id: doc.id,
            title: data.title,
            content: data.content,
            publishedAt: new Date(data.publishedAt),
          });
        });
        setNews(newsData);
      } catch (error) {
        console.error("Error fetching news:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchNews();
  }, []);

  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <h1 className={styles.title}>Noticias Recientes</h1>

        {loading ? (
          <div className={styles.grid}>
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} className="h-48 w-full rounded-lg" />
            ))}
          </div>
        ) : (
          <div className={styles.grid}>
            {news.map((article) => (
              <Card key={article.id} className={styles.card}>
                <CardHeader>
                  <h2 className={styles.cardTitle}>{article.title}</h2>
                  <p className={styles.cardDate}>
                    {new Date(article.publishedAt).toLocaleDateString("es-ES", {
                      year: "numeric",
                      month: "long",
                      day: "numeric",
                    })}
                  </p>
                </CardHeader>
                <CardContent>
                  <p className={styles.cardContent}>
                    {article.content && article.content !== "No hay resumen disponible"
                      ? article.content
                      : "No hay resumen disponible"}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
