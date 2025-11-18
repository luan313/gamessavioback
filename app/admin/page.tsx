'use client'

import { NavHeader } from '@/components/nav-header'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Gamepad2, Tag, Users, TrendingUp } from 'lucide-react'
import Link from 'next/link'

const stats = {
  totalGames: 1247,
  totalCategories: 24,
  totalUsers: 12453,
  totalReviews: 45678,
}

export default function AdminPage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Painel Administrativo</h1>
          <p className="text-muted-foreground">
            Gerencie jogos, categorias e usuários da plataforma
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Jogos</CardTitle>
              <Gamepad2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalGames}</div>
              <p className="text-xs text-muted-foreground">+12 este mês</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Categorias</CardTitle>
              <Tag className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalCategories}</div>
              <p className="text-xs text-muted-foreground">Ativo</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Usuários</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalUsers}</div>
              <p className="text-xs text-muted-foreground">+234 esta semana</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avaliações</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalReviews}</div>
              <p className="text-xs text-muted-foreground">+456 esta semana</p>
            </CardContent>
          </Card>
        </div>

        {/* Management Tabs */}
        <Tabs defaultValue="games" className="space-y-6">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="games">Jogos</TabsTrigger>
            <TabsTrigger value="categories">Categorias</TabsTrigger>
          </TabsList>
          
          <TabsContent value="games">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Gerenciar Jogos</CardTitle>
                    <CardDescription>
                      Adicione, edite ou remova jogos do catálogo
                    </CardDescription>
                  </div>
                  <Link href="/admin/games/new">
                    <Button>
                      <Gamepad2 className="h-4 w-4 mr-2" />
                      Adicionar Jogo
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Lista de todos os jogos cadastrados
                </p>
                <div className="space-y-2">
                  <Link href="/admin/games/1">
                    <div className="flex items-center justify-between p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div>
                        <div className="font-semibold">The Last of Us Part II</div>
                        <div className="text-sm text-muted-foreground">Ação, Aventura • $39.99</div>
                      </div>
                      <Badge>9.5</Badge>
                    </div>
                  </Link>
                  <Link href="/admin/games/2">
                    <div className="flex items-center justify-between p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div>
                        <div className="font-semibold">Red Dead Redemption 2</div>
                        <div className="text-sm text-muted-foreground">Ação, RPG • $59.99</div>
                      </div>
                      <Badge>9.3</Badge>
                    </div>
                  </Link>
                  <Link href="/admin/games/3">
                    <div className="flex items-center justify-between p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div>
                        <div className="font-semibold">God of War</div>
                        <div className="text-sm text-muted-foreground">Ação, Aventura • $49.99</div>
                      </div>
                      <Badge>9.2</Badge>
                    </div>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="categories">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Gerenciar Categorias</CardTitle>
                    <CardDescription>
                      Adicione, edite ou remova categorias
                    </CardDescription>
                  </div>
                  <Link href="/admin/categories/new">
                    <Button>
                      <Tag className="h-4 w-4 mr-2" />
                      Adicionar Categoria
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-4">
                  Lista de todas as categorias cadastradas
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Link href="/admin/categories/1">
                    <div className="p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold">RPG</div>
                        <Badge variant="secondary">1234 jogos</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">Role-Playing Games</p>
                    </div>
                  </Link>
                  <Link href="/admin/categories/2">
                    <div className="p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold">Ação</div>
                        <Badge variant="secondary">2156 jogos</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">Jogos de ação e combate</p>
                    </div>
                  </Link>
                  <Link href="/admin/categories/3">
                    <div className="p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold">Aventura</div>
                        <Badge variant="secondary">1876 jogos</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">Explore mundos e resolva puzzles</p>
                    </div>
                  </Link>
                  <Link href="/admin/categories/4">
                    <div className="p-4 rounded-lg border border-border hover:border-primary transition-colors cursor-pointer">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold">Indie</div>
                        <Badge variant="secondary">3421 jogos</Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">Jogos independentes criativos</p>
                    </div>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
