'use client'

import { NavHeader } from '@/components/nav-header'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Switch } from '@/components/ui/switch'
import { Camera, Save } from 'lucide-react'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function SettingsPage() {
  const router = useRouter()
  const [name, setName] = useState('João Silva')
  const [username, setUsername] = useState('joaosilva')
  const [email, setEmail] = useState('joao@email.com')
  const [bio, setBio] = useState('Gamer apaixonado por RPGs e jogos indie. Sempre procurando as melhores ofertas.')
  
  const [emailNotifications, setEmailNotifications] = useState(true)
  const [priceAlerts, setPriceAlerts] = useState(true)
  const [weeklyDigest, setWeeklyDigest] = useState(false)

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Settings saved:', { name, username, email, bio })
    router.push('/profile')
  }

  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <h1 className="text-3xl font-bold mb-8">Configurações</h1>

        <div className="space-y-6">
          {/* Profile Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Perfil</CardTitle>
              <CardDescription>
                Gerencie suas informações públicas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <form onSubmit={handleSave} className="space-y-6">
                {/* Avatar */}
                <div className="flex items-center gap-4">
                  <Avatar className="h-24 w-24 ring-2 ring-border">
                    <AvatarImage src="/diverse-user-avatars.png" alt="Avatar" />
                    <AvatarFallback>{name.slice(0, 2).toUpperCase()}</AvatarFallback>
                  </Avatar>
                  <Button variant="outline" type="button" className="gap-2">
                    <Camera className="h-4 w-4" />
                    Alterar foto
                  </Button>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="name">Nome</Label>
                    <Input
                      id="name"
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="username">Nome de usuário</Label>
                    <Input
                      id="username"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bio">Bio</Label>
                  <Textarea
                    id="bio"
                    placeholder="Conte um pouco sobre você..."
                    className="resize-none"
                    rows={4}
                    value={bio}
                    onChange={(e) => setBio(e.target.value)}
                  />
                  <p className="text-xs text-muted-foreground">
                    {bio.length}/200 caracteres
                  </p>
                </div>

                <Button type="submit" className="gap-2">
                  <Save className="h-4 w-4" />
                  Salvar Alterações
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Notifications */}
          <Card>
            <CardHeader>
              <CardTitle>Notificações</CardTitle>
              <CardDescription>
                Configure como você deseja receber atualizações
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="email-notifications">Notificações por email</Label>
                  <p className="text-sm text-muted-foreground">
                    Receba emails sobre atividades importantes
                  </p>
                </div>
                <Switch
                  id="email-notifications"
                  checked={emailNotifications}
                  onCheckedChange={setEmailNotifications}
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="price-alerts">Alertas de preço</Label>
                  <p className="text-sm text-muted-foreground">
                    Seja notificado quando jogos atingirem seu preço alvo
                  </p>
                </div>
                <Switch
                  id="price-alerts"
                  checked={priceAlerts}
                  onCheckedChange={setPriceAlerts}
                />
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div className="space-y-0.5">
                  <Label htmlFor="weekly-digest">Resumo semanal</Label>
                  <p className="text-sm text-muted-foreground">
                    Receba um resumo das melhores ofertas da semana
                  </p>
                </div>
                <Switch
                  id="weekly-digest"
                  checked={weeklyDigest}
                  onCheckedChange={setWeeklyDigest}
                />
              </div>
            </CardContent>
          </Card>

          {/* Security */}
          <Card>
            <CardHeader>
              <CardTitle>Segurança</CardTitle>
              <CardDescription>
                Gerencie sua senha e segurança da conta
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="current-password">Senha atual</Label>
                <Input id="current-password" type="password" />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="new-password">Nova senha</Label>
                <Input id="new-password" type="password" />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="confirm-password">Confirmar nova senha</Label>
                <Input id="confirm-password" type="password" />
              </div>

              <Button variant="outline">Alterar Senha</Button>
            </CardContent>
          </Card>

          {/* Danger Zone */}
          <Card className="border-destructive">
            <CardHeader>
              <CardTitle className="text-destructive">Zona de Perigo</CardTitle>
              <CardDescription>
                Ações irreversíveis relacionadas à sua conta
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="destructive">Excluir Conta</Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
