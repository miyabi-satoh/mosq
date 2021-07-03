import { apiAuth, TUser } from "api";
import { logger } from "helper";
import React, { useEffect, useState } from "react";
import { useContext } from "react";
import { createContext } from "react";
import { useLocation } from "react-router-dom";

interface IAuthContext {
  currentUser: TUser | null | undefined;
  login: (username: string, password: string) => void;
  logout: () => void;
}

const AuthContext = createContext<IAuthContext>({
  currentUser: undefined,
  login: (username: string, password: string) => {
    throw Error("login method is undefined.");
  },
  logout: () => {
    throw Error("logout method is undefined.");
  },
});

function useAuth() {
  return useContext(AuthContext);
}

function AuthProvider(props: React.PropsWithChildren<{}>) {
  const location = useLocation();
  const [currentUser, setCurrentUser] = useState<TUser | null | undefined>(
    undefined
  );

  const login = async (username: string, password: string) => {
    try {
      const user = await apiAuth.login(username, password);
      setCurrentUser(user);
    } catch (error) {
      setCurrentUser(null);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiAuth.logout();
    } catch (error) {
    } finally {
      setCurrentUser(undefined);
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
          logger(user);
          setCurrentUser(user);
        }
      }
    };
    f();

    return () => {
      unmounted = true;
    };
  }, [location]);

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        login,
        logout,
      }}
    >
      {props.children}
    </AuthContext.Provider>
  );
}

export { useAuth, AuthProvider };
