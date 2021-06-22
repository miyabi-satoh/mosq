import { apiAuth, TUser } from "api";
import React, { useEffect, useState } from "react";
import { useContext } from "react";
import { createContext } from "react";

interface IAuthContext {
  currentUser: TUser | null | undefined;
  login: (username: string, password: string) => void;
}

const AuthContext = createContext<IAuthContext>({
  currentUser: undefined,
  login: (username: string, password: string) => {
    throw Error("login method is undefined.");
  },
});

function useAuth() {
  return useContext(AuthContext);
}

function AuthProvider(props: React.PropsWithChildren<{}>) {
  const [currentUser, setCurrentUser] =
    useState<TUser | null | undefined>(undefined);

  const login = async (username: string, password: string) => {
    try {
      const user = await apiAuth.login(username, password);
      setCurrentUser(user);
    } catch (error) {
      setCurrentUser(null);
      throw error;
    }
  };

  useEffect(() => {
    let unmounted = false;

    const f = async () => {
      let user;
      try {
        user = await apiAuth.me();
        if (!user.id) {
          throw Error();
        }
      } catch (error) {
        user = undefined;
      } finally {
        if (!unmounted) {
          setCurrentUser(user);
        }
      }
    };
    f();

    return () => {
      unmounted = true;
    };
  }, []);

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        login,
      }}
    >
      {props.children}
    </AuthContext.Provider>
  );
}

export { useAuth, AuthProvider };
