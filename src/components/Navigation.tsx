"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { onAuthStateChanged, User } from "firebase/auth";
import { auth } from "@/lib/firebase";
import LogoutButton from "./LogoutButton";
import styles from "./Navigation.module.css";

export default function Navigation() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
    });
    return () => unsubscribe();
  }, []);

  return (
    <nav className={styles.navbar}>
      <Link href="/" className={styles.link}>
        Inicio
      </Link>
      {user ? (
        <LogoutButton />
      ) : (
        <>
          <Link href="/login" className={styles.link}>
            Iniciar Sesión
          </Link>
          <Link href="/register" className={styles.link}>
            Registrarse
          </Link>
        </>
      )}
    </nav>
  );
}
